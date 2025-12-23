from typing import Annotated, List, Optional, Union
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError

from app.core.config import settings
from app.services.user import user_service
from app.schemas.user import UserRole

# 1. Định nghĩa OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/v1/users/login")


# 2. Hàm Dependency cốt lõi: Lấy User hiện tại từ Token
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Giải mã Token
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

    except (JWTError, ValidationError):
        raise credentials_exception

    # Gọi Service tìm User
    user = await user_service.get_user_by_email_for_auth(email)

    if not user:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return user


# 3. Hàm check quyền (Role)
def require_roles(allowed_roles: List[Union[str, UserRole]]):
    """
    Dependency trả về user nếu user đó có role nằm trong danh sách cho phép.
    Ví dụ dùng: Depends(require_roles(["admin", "teacher"]))
    """

    async def _role_checker(current_user=Depends(get_current_user)):
        # So sánh role của user với danh sách cho phép
        # (Chuyển về string để so sánh cho an toàn nếu dùng Enum)
        user_role_str = str(current_user.role)
        allowed_strs = [str(r) for r in allowed_roles]

        if user_role_str not in allowed_strs:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )
        return current_user

    return _role_checker


async def require_authenticated(current_user=Depends(get_current_user)):
    return current_user


async def get_current_admin(
    current_user=Depends(require_roles(["admin", "super_admin"]))
):
    return current_user
