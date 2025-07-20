from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import emails

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="Email Analyzer API",
    description="API cho hệ thống phân tích và phát hiện email lừa đảo",
    version="1.0.0",
)

# Cấu hình CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong môi trường production nên giới hạn các origin được phép
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký các router
app.include_router(emails.router, prefix="/api/emails", tags=["emails"])

# Kiểm tra endpoint
@app.get("/")
def read_root():
    return {"message": "Email Analyzer API đang chạy"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
