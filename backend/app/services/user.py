from fastapi import HTTPException, status
from datetime import timedelta
from app.repositories.user import user_repo
from app.core.security import verify_password, create_access_token, hash_password
from app.schemas.user import (
    CreateUserRequest,
    UpdateUserRequest,
    LoginRequest,
    LoginResponse,
)
from app.core.config import settings


class UserService:
    async def login(self, data: LoginRequest) -> LoginResponse:
        user = await user_repo.get_by_email(data.email)

        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email hoặc mật khẩu không chính xác.",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Tài khoản đã bị khóa."
            )

        access_token = create_access_token(
            subject=user.id,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user=user,  # Trả về cả object User (Pydantic sẽ tự map)
        )

    async def create_user(self, data: CreateUserRequest):
        # 1. Check trùng email
        existing_user = await user_repo.get_by_email(data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email này đã được đăng ký.",
            )

        # 2. Gọi Repo tạo mới
        return await user_repo.create(data)

    async def get_user_by_id(self, user_id: str):
        user = await user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def list_users(self, skip: int, limit: int):
        return await user_repo.list_users(skip=skip, limit=limit)

    async def update_user(self, user_id: str, data: UpdateUserRequest):
        # 1. Kiểm tra user tồn tại
        await self.get_user_by_id(user_id)

        # 2. Xử lý Update Password riêng (Nếu có gửi password mới)
        if data.password:
            # Hash mật khẩu mới
            hashed = hash_password(data.password)
            # Gọi hàm chuyên biệt trong repo để update cột password_hash
            await user_repo.update_password(user_id, hashed)

            # QUAN TRỌNG: Set password về None để hàm update chung bên dưới
            # không cố gắng update cột 'password' (gây lỗi Prisma)
            data.password = None

        # 3. Gọi Repo update các thông tin còn lại (name, role, is_active...)
        return await user_repo.update(user_id, data)

    async def delete_user(self, user_id: str):
        await self.get_user_by_id(user_id)
        return await user_repo.delete(user_id)


user_service = UserService()
