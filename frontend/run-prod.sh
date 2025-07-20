#!/bin/bash

echo "Khởi động môi trường production cho frontend Email Analyzer..."

# Kiểm tra cài đặt Docker
if ! command -v docker &> /dev/null; then
    echo "Lỗi: Docker chưa được cài đặt. Vui lòng cài đặt Docker trước khi tiếp tục."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Lỗi: Docker Compose chưa được cài đặt. Vui lòng cài đặt Docker Compose trước khi tiếp tục."
    exit 1
fi

# Kiểm tra xem .env đã tồn tại chưa
if [ ! -f ".env" ]; then
    echo "Tạo file .env mặc định..."
    cat > .env << EOF
VUE_APP_API_URL=http://localhost:8000/api
VUE_APP_TITLE=Email Analyzer System
EOF
fi

# Kiểm tra container đang chạy
if docker ps --format '{{.Names}}' | grep -q "^email_analyzer_frontend$"; then
    echo "Container 'email_analyzer_frontend' đang chạy. Dừng docker-compose..."
    docker-compose down frontend-prod
fi

echo "Khởi động môi trường production với Docker..."
docker-compose up -d frontend-prod --build

echo "Đợi container khởi động..."
sleep 5

if docker ps | grep -q "email_analyzer_frontend"; then
    echo "Frontend đang chạy tại http://localhost:8080"
else
    echo "Lỗi: Frontend không khởi động. Kiểm tra logs:"
    docker-compose logs frontend-prod
fi 