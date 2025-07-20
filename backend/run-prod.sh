#!/bin/bash

echo "Khởi động môi trường production cho Email Analyzer API..."

# Kiểm tra cài đặt Docker
if ! command -v docker &> /dev/null; then
    echo "Lỗi: Docker chưa được cài đặt. Vui lòng cài đặt Docker trước khi tiếp tục."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Lỗi: Docker Compose chưa được cài đặt. Vui lòng cài đặt Docker Compose trước khi tiếp tục."
    exit 1
fi

# Kiểm tra xem .env.prod đã tồn tại chưa
if [ ! -f ".env.prod" ]; then
    echo "Lỗi: File .env.prod không tồn tại. Vui lòng tạo file này trước khi tiếp tục."
    exit 1
fi

# Copy file .env.prod thành .env cho Docker Compose
cp .env.prod .env

# Tạo và khởi động các container
echo "Khởi động các container với Docker Compose..."
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

# Kiểm tra container API đã chạy chưa
echo "Đợi container API khởi động..."
sleep 5

if docker ps | grep -q "email_analyzer_api"; then
    echo "API đang chạy tại http://localhost:8000"
    
    # Tạo bảng trong database nếu chưa tồn tại
    echo "Kiểm tra và tạo bảng database..."
    docker exec -it email_analyzer_api python -c "from database.session import Base, engine; Base.metadata.create_all(bind=engine); print('Tạo bảng database thành công')"
else
    echo "Lỗi: API không khởi động. Kiểm tra logs:"
    docker-compose logs api
fi 