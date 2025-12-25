from typing import Annotated, List, Optional, Union
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.core.config import settings
from app.services.user import user_service
from app.repositories.session import session_repo
from app.schemas.user import UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/v1/users/login")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        session_id: str = payload.get("jti")

        if session_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    session = await session_repo.get_by_id(session_id)
    if not session or not session.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or logged out",
        )

    if not session.user.is_active:
        raise HTTPException(status_code=400, detail="User account is locked")

    return session.user


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


async def get_current_jti(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload.get("jti")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
