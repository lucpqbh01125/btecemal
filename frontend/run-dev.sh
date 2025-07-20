#!/bin/bash

echo "Khởi động môi trường development cho frontend Email Analyzer..."

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
if docker ps --format '{{.Names}}' | grep -q "^email_analyzer_frontend_dev$"; then
    docker-compose down frontend-dev
fi

echo "Khởi động môi trường development với Docker..."
docker-compose up -d frontend-dev

# Chỉnh sửa lệnh bên trong container để bỏ qua ESLint
docker exec email_analyzer_frontend_dev sh -c "sed -i 's/vue-cli-service serve/vue-cli-service serve --no-lint/g' /app/package.json"

echo "Frontend đang chạy tại http://localhost:8088"
docker-compose logs -f frontend-dev 
