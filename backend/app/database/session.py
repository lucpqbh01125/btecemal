from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Tải biến môi trường
load_dotenv()

# Thông tin kết nối database từ biến môi trường
DB_HOST = os.getenv("MYSQL_HOST", "")
DB_USER = os.getenv("MYSQL_USER", "")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
DB_NAME = os.getenv("MYSQL_DATABASE", "")
DB_PORT = int(os.getenv("MYSQL_PORT", ""))

# Tạo URL kết nối
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Tạo engine kết nối đến database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_timeout=30,
    max_overflow=10,
    echo=True  # Để debug connection
)

# Tạo session để tương tác với database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class cho các model
Base = declarative_base()

# Hàm tạo database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Hàm test connection
def test_db_connection():
    try:
        connection = engine.connect()
        print(f"✅ Kết nối database thành công: {DB_HOST}:{DB_PORT}")
        connection.close()
        return True
    except Exception as e:
        print(f"❌ Lỗi kết nối database: {e}")
        return False 