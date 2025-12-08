from fastapi import APIRouter
from app.api.api_v1.endpoints import auth, students, face  # <--- (1) Import thêm face

api_router = APIRouter()

# Các router cũ
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(students.router, prefix="/students", tags=["Students"])

# (2) Đăng ký router mới cho FaceID
api_router.include_router(face.router, prefix="/face", tags=["Face Recognition"])
