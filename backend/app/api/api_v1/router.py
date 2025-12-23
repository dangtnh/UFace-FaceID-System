from app.api.api_v1.endpoints import student
from fastapi import APIRouter
from app.api.api_v1.endpoints import user, face, student

api_router = APIRouter()

# 1. Router cho xác thực (Login)
api_router.include_router(user.router, prefix="/users", tags=["Users"])

# 2. Router cho quản lý sinh viên (Đăng ký mới, có lưu Email + Train AI)
api_router.include_router(student.router, prefix="/students", tags=["Students"])

# 3. Router cho nhận diện khuôn mặt (Điểm danh/Check-in)
api_router.include_router(face.router, prefix="/face", tags=["Face Recognition"])
