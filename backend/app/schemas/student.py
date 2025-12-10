from pydantic import BaseModel, EmailStr
from datetime import datetime


# Class này định nghĩa dữ liệu từ Frontend gửi lên
# Bắt buộc phải có schoolEmail
class StudentCreate(BaseModel):
    fullName: str
    studentId: str
    schoolEmail: EmailStr  # Dùng EmailStr để tự động check định dạng a@b.c


# Class này định nghĩa dữ liệu trả về cho Frontend sau khi lưu xong
class StudentResponse(BaseModel):
    id: int
    fullName: str
    studentId: str
    schoolEmail: str
    status: str
    createdAt: datetime

    class Config:
        from_attributes = True
