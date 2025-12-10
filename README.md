# 🎭 UFace - FaceID System

Hệ thống điểm danh và nhận diện khuôn mặt tự động (Automated Face Recognition System) được xây dựng trên nền tảng **FastAPI**, **PostgreSQL** và **Docker**.

## 🚀 Tính năng chính
- Nhận diện khuôn mặt thời gian thực (Real-time Face Recognition).
- API quản lý danh sách nhân viên/người dùng.
- Tự động mã hóa khuôn mặt thành Vector và lưu trữ vào Database.
- Hệ thống đóng gói hoàn chỉnh với Docker & Docker Compose.

## 🛠 Yêu cầu hệ thống (Prerequisites)
Để chạy được dự án, máy tính cần cài đặt sẵn:
- **Git**
- **Docker** & **Docker Compose** (phiên bản mới nhất)

---

## ⚙️ Hướng dẫn Cài đặt & Khởi chạy (Quick Start)
git clone [https://github.com/dangtnh/UFace-FaceID-System.git](https://github.com/dangtnh/UFace-FaceID-System.git)
cd UFace-FaceID-System

cp .env.example .env

mkdir -p data/images
mkdir -p data/vectors

docker compose -f deploy/docker-compose.dev.yml up -d --build

