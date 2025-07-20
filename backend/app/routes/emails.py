from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from dependencies.deps import get_db
from schemas.email import EmailResponse, EmailAnalyzeRequest, EmailAnalyzeResponse, EmailStatsResponse, EmailBatchAnalyzeResponse
from models.email import Email
from services.email_analyzer import EmailAnalyzer

router = APIRouter()
email_analyzer = EmailAnalyzer()

@router.get("/stats", response_model=EmailStatsResponse)
async def get_email_stats(db: Session = Depends(get_db)):
    """
    Lấy thống kê về email trong hệ thống.
    """
    # Tính tổng số email
    total = db.query(Email).count()
    
    # Tính số lượng email theo từng loại
    categories = {}
    for category_name in ["safe", "suspicious", "spam", "phishing", "unknown"]:
        count = db.query(Email).filter(Email.category == category_name).count()
        percentage = (count / total * 100) if total > 0 else 0
        categories[category_name] = {
            "count": count,
            "percentage": round(percentage, 1)
        }
    
    # Lấy xu hướng gần đây (7 ngày)
    seven_days_ago = datetime.now() - timedelta(days=7)
    recent_emails = db.query(Email).filter(
        Email.received_time >= seven_days_ago
    ).order_by(Email.received_time).all()
    
    # Tính số lượng email theo ngày và phân loại
    trend_data = []
    dates = {}
    
    for email in recent_emails:
        date_str = email.received_time.strftime("%Y-%m-%d")
        if date_str not in dates:
            dates[date_str] = {"date": date_str, "safe": 0, "suspicious": 0, "spam": 0, "phishing": 0, "unknown": 0}
        dates[date_str][email.category] += 1
    
    trend_data = list(dates.values())
    trend_data.sort(key=lambda x: x["date"])
    
    return {
        "total": total,
        "categories": categories,
        "recent_trend": trend_data
    }

@router.get("/", response_model=List[EmailResponse])
async def get_emails(
    category: Optional[str] = None, 
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách email với bộ lọc tùy chọn.
    """
    query = db.query(Email)
    
    # Áp dụng filter nếu có
    if category and category != "all":
        query = query.filter(Email.category == category)
    
    # Sắp xếp theo thời gian nhận, mới nhất đầu tiên
    query = query.order_by(Email.received_time.desc())
    
    # Phân trang
    emails = query.offset(offset).limit(limit).all()
    
    return emails

@router.post("/analyze", response_model=EmailAnalyzeResponse)
async def analyze_email(
    request: EmailAnalyzeRequest,
    db: Session = Depends(get_db)
):
    """
    Phân tích một email và trả về kết quả phân tích.
    """
    try:
        # Phân tích email
        analysis = email_analyzer.analyze_email(
            title=request.title,
            content=request.content,
            sender=request.sender
        )
        
        return {
            "success": True,
            "data": analysis,
            "message": "Phân tích email thành công"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Lỗi khi phân tích email: {str(e)}"
        }

@router.post("/analyze-batch", response_model=EmailBatchAnalyzeResponse)
async def analyze_batch(
    limit: Optional[int] = Query(None, description="Số lượng email muốn phân tích, để trống để phân tích tất cả"),
    db: Session = Depends(get_db)
):
    """
    Phân tích hàng loạt email chưa được phân loại.
    """
    try:
        # Lấy các email chưa được phân loại
        query = db.query(Email).filter(Email.category == "unknown")
        
        # Giới hạn số lượng nếu có
        if limit is not None and limit > 0:
            query = query.limit(limit)
        
        emails = query.all()
        count = 0
        
        # Phân tích từng email
        for email in emails:
            # Phân tích email
            analysis = email_analyzer.analyze_email(
                title=email.title,
                content=email.content,
                sender=email.from_email
            )
            
            # Cập nhật kết quả vào database
            email.category = analysis["category"]
            email.category_id = analysis["category_id"]
            email.confidence_score = analysis["confidence_score"]
            email.level = analysis["level"]
            email.suspicious_indicators = analysis["suspicious_indicators"]
            
            count += 1
        
        # Lưu các thay đổi vào database
        db.commit()
        
        return {
            "success": True,
            "processed_count": count,
            "message": f"Đã phân tích thành công {count} email"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi phân tích hàng loạt: {str(e)}"
        ) 