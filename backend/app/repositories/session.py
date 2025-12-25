# app/repositories/session.py
from datetime import datetime
from typing import Optional

from app.core.database import prisma


class SessionRepository:
    async def create(
        self, user_id: str, user_agent: str | None, ip: str | None, expires_at: datetime
    ):
        """
        Tạo phiên đăng nhập mới.
        Lưu ý: Dùng 'user_session' (snake_case) vì Prisma Python tự đổi tên model UserSession.
        """
        return await prisma.usersession.create(
            data={
                "user_id": user_id,
                "user_agent": user_agent,
                "ip": ip,
                "expires_at": expires_at,
                "is_active": True,
            }
        )

    async def get_by_id(self, session_id: str):
        """
        Lấy thông tin session theo ID (jti).
        Dùng include={'user': True} để lấy luôn thông tin User sở hữu session đó.
        """
        return await prisma.usersession.find_unique(
            where={"id": session_id}, include={"user": True}
        )

    async def revoke(self, session_id: str):
        """
        Hủy session (Logout) -> Chỉ đơn giản là set is_active = False.
        """
        return await prisma.usersession.update(
            where={"id": session_id}, data={"is_active": False}
        )


session_repo = SessionRepository()
