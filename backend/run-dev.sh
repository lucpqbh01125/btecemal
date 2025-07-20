#!/bin/bash

COMPOSE_FILES="-f docker-compose.yml -f docker-compose.dev.yml"

if docker ps --format '{{.Names}}' | grep -q "^email_analyzer_api$"; then
    echo "Container 'email_analyzer_api' đang chạy. Dừng docker-compose..."
    docker-compose $COMPOSE_FILES down
    exit 0
fi

echo "Container 'email_analyzer_api' chưa chạy. Khởi động môi trường development..."
# Sử dụng file .env.dev cho môi trường development

echo "Khởi động docker-compose..."
docker-compose $COMPOSE_FILES up -d --build

# Đợi MySQL trên container db sẵn sàng
echo "Đợi MySQL sẵn sàng trên container db..."
until docker exec email_analyzer_db mysqladmin ping -h"email_analyzer_db" --silent || [ $? -eq 1 ]; do
    sleep 2
    echo "Chưa sẵn sàng, thử lại..."
    # Nếu container bị lỗi, thoát
    if ! docker ps | grep -q email_analyzer_db; then
        echo "Container MySQL không chạy. Kiểm tra logs để biết thêm chi tiết."
        docker-compose $COMPOSE_FILES logs db
        exit 1
    fi
done

echo "Đợi container email_analyzer_api khởi động..."
while ! docker exec email_analyzer_api ls >/dev/null 2>&1; do
    sleep 1
    # Nếu container bị lỗi, thoát
    if ! docker ps | grep -q email_analyzer_api; then
        echo "Container API không chạy. Kiểm tra logs để biết thêm chi tiết."
        docker-compose $COMPOSE_FILES logs api
        exit 1
    fi
done

echo "Tạo bảng database (nếu chưa có)..."
docker exec email_analyzer_api python -c "
import sys, os, glob, importlib
sys.path.insert(0, '/app')
try:
    from database.session import Base, engine
    models_dir = os.path.join('/app', 'models')
    for file in glob.glob(os.path.join(models_dir, '*.py')):
        name = os.path.splitext(os.path.basename(file))[0]
        if name != '__init__':
            importlib.import_module(f'models.{name}')
    Base.metadata.create_all(bind=engine)
    print('Đã tạo bảng thành công (hoặc đã tồn tại)')
except Exception as e:
    print('Lỗi khi tạo bảng:', e)
    sys.exit(1)
"

echo "Môi trường development đã sẵn sàng tại http://localhost:8000"
docker-compose $COMPOSE_FILES logs -f api 