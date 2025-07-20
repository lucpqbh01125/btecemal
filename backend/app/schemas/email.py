from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime

class EmailBase(BaseModel):
    """Schema cơ bản cho email"""
    title: str
    content: str
    from_email: str
    to_email: str
    received_time: datetime

class EmailCreate(EmailBase):
    """Schema cho việc tạo mới email"""
    pass

class EmailAnalysis(BaseModel):
    """Kết quả phân tích email"""
    category: str
    category_id: int
    confidence_score: float
    level: str
    suspicious_indicators: Optional[Dict[str, Any]] = None
    recommendation: Optional[str] = None

class EmailResponse(EmailBase):
    """Schema cho việc trả về thông tin email"""
    id: int
    category: str
    category_id: int
    suspicious_indicators: Optional[Dict[str, Any]] = None
    confidence_score: float
    level: str
    created_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

class EmailBatchAnalyzeRequest(BaseModel):
    """Request để phân tích nhiều email cùng lúc"""
    limit: Optional[int] = None

class EmailAnalyzeRequest(BaseModel):
    """Request để phân tích một email"""
    title: str
    content: str
    sender: str

class EmailAnalyzeResponse(BaseModel):
    """Response cho kết quả phân tích email"""
    success: bool
    data: Optional[EmailAnalysis] = None
    message: Optional[str] = None

class EmailBatchAnalyzeResponse(BaseModel):
    """Response cho kết quả phân tích nhiều email"""
    success: bool
    processed_count: int
    message: str

class EmailStatsResponse(BaseModel):
    """Response cho thống kê email"""
    total: int
    categories: Dict[str, Dict[str, Union[int, float]]]
    recent_trend: Optional[List[Dict[str, Any]]] = None 