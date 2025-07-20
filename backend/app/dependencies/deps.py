from database.session import SessionLocal
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Generator, Optional

# Database dependency
def get_db() -> Generator:
    """
    Dependency để lấy database session cho các route.
    Hàm này được sử dụng như một FastAPI dependency injection
    để tạo và quản lý session kết nối đến database.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 