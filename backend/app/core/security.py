from datetime import datetime, timedelta, timezone
from typing import Any, Union
from uuid import uuid4
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

# 1. Cấu hình Hash Pass
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# 2. Cấu hình JWT
def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """Tạo Access Token (ngắn hạn - thường 15-30p)"""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # Payload chứa thông tin user
    to_encode = {
        "sub": str(subject),  # Subject (thường là User ID)
        "exp": expire,  # Thời gian hết hạn
        "iat": datetime.now(timezone.utc),  # Thời gian phát hành
        "type": "access",
        "jti": str(uuid4()),  # Unique ID cho token này
    }

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any]) -> str:
    """Tạo Refresh Token (dài hạn - dùng config đã cài)"""
    # SỬA LẠI: Dùng biến từ config thay vì fix cứng 7 ngày
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "refresh",  # Đánh dấu đây là refresh token
        "jti": str(uuid4()),
    }

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> dict:
    """Giải mã token để lấy thông tin bên trong (payload)"""
    # Thư viện jose sẽ tự kiểm tra hạn sử dụng (exp), nếu hết hạn nó sẽ báo lỗi
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
