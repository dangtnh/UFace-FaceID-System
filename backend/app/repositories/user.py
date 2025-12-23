from typing import Optional, List
from app.core.database import prisma  # Đảm bảo bạn đã có file này
from app.schemas.user import CreateUserRequest, UpdateUserRequest
from app.core.security import hash_password  # Import từ file security vừa viết


class UserRepository:
    async def create(self, data: CreateUserRequest):
        """Tạo mới một user với mật khẩu đã được mã hóa"""
        # 1. Mã hóa mật khẩu
        hashed = hash_password(data.password)

        # 2. Lưu vào DB
        return await prisma.user.create(
            data={
                "email": data.email,
                "name": data.name,
                "password_hash": hashed,  # Lưu pass đã mã hóa
                "role": data.role.value,  # Lấy value của Enum (ví dụ "ADMIN")
                "is_active": data.is_active,
            }
        )

    async def get_by_id(self, user_id: str):
        """Tìm user theo ID"""
        return await prisma.user.find_unique(where={"id": user_id})

    async def get_by_email(self, email: str):
        """Tìm user theo Email (Dùng cho Login)"""
        return await prisma.user.find_unique(where={"email": email})

    async def list_users(self, skip: int = 0, limit: int = 100):
        """Lấy danh sách user (Phân trang)"""
        return await prisma.user.find_many(
            skip=skip, take=limit, order={"created_at": "desc"}
        )

    async def update(self, user_id: str, data: UpdateUserRequest):
        """Cập nhật thông tin user"""
        # exclude_unset=True: Chỉ update những trường user gửi lên (tránh ghi đè None)
        update_data = data.model_dump(exclude_unset=True)

        return await prisma.user.update(where={"id": user_id}, data=update_data)

    async def update_password(self, user_id: str, new_hash: str):
        """Cập nhật mật khẩu mới (đã hash)"""
        return await prisma.user.update(
            where={"id": user_id}, data={"password_hash": new_hash}
        )

    async def delete(self, user_id: str, soft: bool = True):
        """Xóa user (Mặc định là xóa mềm - Soft Delete)"""
        if soft:
            # Soft delete: Chỉ set is_active = False
            return await prisma.user.update(
                where={"id": user_id}, data={"is_active": False}
            )
        else:
            # Hard delete: Xóa vĩnh viễn khỏi DB
            return await prisma.user.delete(where={"id": user_id})


user_repo = UserRepository()
