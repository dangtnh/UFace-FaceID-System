from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from enum import Enum
from datetime import datetime


# Định nghĩa Role khớp với Prisma Enums
class UserRole(str, Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"


# --- Base Schema (Chứa các trường chung) ---
class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    role: UserRole = UserRole.student
    is_active: bool = True


# --- Dùng cho lúc Đăng ký (Register/Create) ---
class CreateUserRequest(UserBase):
    password: str


# --- Dùng cho lúc Sửa user (Update) ---
class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


# --- Dùng cho lúc Đổi mật khẩu ---
class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


# --- Dùng để trả dữ liệu về (Response) ---
class UserResponse(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime

    # Config này giúp Pydantic đọc được dữ liệu từ Prisma object
    model_config = ConfigDict(from_attributes=True)


# --- Dùng cho lúc Login ---
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
