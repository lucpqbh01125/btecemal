from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON
from sqlalchemy.sql import func
from database.session import Base

class Email(Base):
    """
    Model cho bảng incoming_emails để lưu trữ thông tin email và kết quả phân tích
    """
    __tablename__ = 'incoming_emails'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    from_email = Column(String(255), nullable=False)
    to_email = Column(String(255), nullable=False)
    received_time = Column(DateTime, nullable=False, index=True)
    
    # Thông tin phân loại
    category = Column(String(50), default='unknown', nullable=True, index=True)
    category_id = Column(Integer, default=1, nullable=True)
    suspicious_indicators = Column(JSON, nullable=True)
    confidence_score = Column(Float, default=0.0, nullable=True, index=True)
    level = Column(String(20), default='', nullable=True, index=True)
    
    # Metadata
    created_at = Column(DateTime, default=func.now(), nullable=True)

    @staticmethod
    def get_category_name(category_id):
        """Lấy tên danh mục từ category_id"""
        categories = {
            1: 'unknown',
            2: 'safe',
            3: 'suspicious',
            4: 'spam',
            5: 'phishing'
        }
        return categories.get(category_id, 'unknown')
    
    @staticmethod
    def get_category_id(category_name):
        """Lấy category_id từ tên danh mục"""
        categories = {
            'unknown': 1,
            'safe': 2,
            'suspicious': 3,
            'spam': 4,
            'phishing': 5
        }
        return categories.get(category_name.lower(), 1) 