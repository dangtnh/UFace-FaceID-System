# 🎭 UFace - FaceID System

Hệ thống điểm danh và nhận diện khuôn mặt tự động (Automated Face Recognition System) được xây dựng trên nền tảng **FastAPI**, **PostgreSQL** và **Docker**.

# 🚀 Tính năng chính
- Nhận diện khuôn mặt thời gian thực (Real-time Face Recognition).
- API quản lý danh sách nhân viên/người dùng.
- Tự động mã hóa khuôn mặt thành Vector và lưu trữ vào Database.
- Hệ thống đóng gói hoàn chỉnh với Docker & Docker Compose.

# 🛠 Yêu cầu hệ thống (Prerequisites)
Để chạy được dự án, máy tính cần cài đặt sẵn:
- **Git**
- **Docker** & **Docker Compose** (phiên bản mới nhất)

---

# ⚙️ Hướng dẫn Cài đặt & Khởi chạy (Quick Start)
## 1. Clone
```
git clone [https://github.com/dangtnh/UFace-FaceID-System.git]
cd UFace-FaceID-System
```

## 2. Tạo môi trường
```
cp .env.example .env

mkdir -p data/images
mkdir -p data/vectors
```

## 3. Docker commands
- Build from scratch
```
docker compose up --build -d
```

- Create and draw tables in Database
```
docker compose run --rm prisma_studio npx prisma migrate dev --name init
```

```
docker compose run --rm prisma_studio npx prisma migrate dev --name init --skip-generate

docker compose restart backend```
==========
- Turn on all container and turn off all the container
```
docker compose up -d
docker compose down```

==========
- Delete all the data in container
```
docker compose down -v```

