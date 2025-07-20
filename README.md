# Email Analyzer System

Hệ thống phân tích và phát hiện email lừa đảo (phishing) sử dụng FastAPI, Vue.js và Docker.

## Cấu trúc dự án

```
projectemail/
├── backend/                    # Backend FastAPI
│   ├── app/                    # Mã nguồn chính
│   │   ├── database/           # Kết nối database
│   │   ├── dependencies/       # Các dependency injection
│   │   ├── models/             # Mô hình dữ liệu (SQLAlchemy)
│   │   ├── routes/             # API endpoints
│   │   ├── schemas/            # Schema validation (Pydantic)
│   │   ├── services/           # Business logic
│   │   └── utils/              # Các tiện ích
│   ├── docker-compose.yml      # Cấu hình Docker Compose
│   ├── docker-compose.dev.yml  # Cấu hình Docker Compose cho môi trường dev
│   ├── docker-compose.prod.yml # Cấu hình Docker Compose cho môi trường production
│   ├── .env.dev               # Biến môi trường cho development
│   ├── .env.prod              # Biến môi trường cho production
│   ├── Dockerfile             # Dockerfile cho backend
│   ├── requirements.txt       # Các gói Python cần thiết
│   ├── run-dev.sh             # Script để chạy môi trường dev
│   └── run-prod.sh            # Script để chạy môi trường production
└── frontend/                  # Frontend Vue.js
    ├── public/                # Static assets
    ├── src/                   # Mã nguồn Vue
    │   ├── api/               # API clients
    │   ├── assets/            # Assets (CSS, hình ảnh)
    │   ├── components/        # Vue components
    │   ├── router/            # Vue Router
    │   ├── store/             # Vuex store
    │   ├── utils/             # Các tiện ích
    │   └── views/             # Các trang
    ├── docker-compose.yml     # Cấu hình Docker Compose
    ├── docker-compose.prod.yml # Cấu hình Docker Compose cho production
    ├── .env                   # Biến môi trường cho development
    ├── .env.prod              # Biến môi trường cho production
    ├── Dockerfile             # Dockerfile cho frontend
    ├── nginx.conf             # Cấu hình nginx cho production
    ├── package.json           # Cấu hình npm
    ├── vue.config.js          # Cấu hình Vue CLI
    ├── run-dev.sh             # Script để chạy môi trường dev
    └── run-prod.sh            # Script để chạy môi trường production
```

## Tính năng

- Phân tích và phát hiện email lừa đảo (phishing), spam
- Dashboard hiển thị thống kê về các email đã phân tích
- Công cụ kiểm tra email để người dùng có thể kiểm tra email đáng ngờ
- Hỗ trợ tìm kiếm và lọc email theo nhiều tiêu chí
- Phân tích tự động hàng loạt email

## Cài đặt và chạy

### Yêu cầu

- Docker và Docker Compose
- Node.js và npm (để phát triển frontend)
- Python 3.9+ (để phát triển backend)

### Khởi động backend (môi trường development)

```bash
cd projectemail/backend
./run-dev.sh
```

Backend API sẽ chạy tại: http://localhost:8000

### Khởi động frontend (môi trường development)

```bash
cd projectemail/frontend
./run-dev.sh
```

Frontend sẽ chạy tại: http://localhost:8081

### Khởi động backend (môi trường production)

```bash
cd projectemail/backend
./run-prod.sh
```

Backend API sẽ chạy tại: http://localhost:8000

### Khởi động frontend (môi trường production)

```bash
cd projectemail/frontend
./run-prod.sh
```

Frontend sẽ chạy tại: http://localhost:8080

## API Endpoints

- `GET /api/emails/stats`: Lấy thống kê về email
- `GET /api/emails`: Lấy danh sách email (hỗ trợ phân trang và lọc)
- `POST /api/emails/analyze`: Phân tích một email
- `POST /api/emails/analyze-batch`: Phân tích hàng loạt email

## Công nghệ sử dụng

### Backend
- FastAPI (framework API)
- SQLAlchemy (ORM)
- Pydantic (data validation)
- PyMySQL (MySQL connector)
- Docker (containerization)

### Frontend
- Vue.js 2 (framework frontend)
- Vuex (state management)
- Vue Router (routing)
- Bootstrap-Vue (UI components)
- Axios (HTTP client)
- ApexCharts (biểu đồ thống kê) 