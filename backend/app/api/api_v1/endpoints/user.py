from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.services.user import user_service
from app.core.session import (
    require_authenticated,
    require_roles,
    get_current_admin,
    get_current_jti,
)
from app.schemas.user import (
    CreateUserRequest,
    UpdateUserRequest,
    UserResponse,
    LoginRequest,
    LoginResponse,
    UserRole,
)

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest, request: Request) -> Any:
    # 1. Lấy User-Agent (Trình duyệt/Thiết bị)
    user_agent = request.headers.get("user-agent")

    # 2. Lấy IP Address
    ip = request.client.host if request.client else None

    return await user_service.login(payload, user_agent=user_agent, ip=ip)


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    session_id: str = Depends(get_current_jti), _: Any = Depends(require_authenticated)
) -> Any:
    await user_service.logout(session_id)
    return {"message": "Đăng xuất thành công"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user=Depends(require_authenticated)) -> Any:
    return current_user


@router.patch("/me", response_model=UserResponse)
async def update_me(
    payload: UpdateUserRequest, current_user=Depends(require_authenticated)
) -> Any:
    return await user_service.update_user(current_user.id, payload)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: CreateUserRequest, _=Depends(require_roles(["admin"]))
) -> Any:
    return await user_service.create_user(payload)


@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0, limit: int = 100, _=Depends(require_roles(["admin"]))
) -> Any:
    return await user_service.list_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, _=Depends(require_roles(["admin"]))) -> Any:
    return await user_service.get_user_by_id(user_id)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str, payload: UpdateUserRequest, _=Depends(require_roles(["admin"]))
) -> Any:
    return await user_service.update_user(user_id, payload)


@router.delete("/{user_id}")
async def delete_user(user_id: str, _=Depends(require_roles(["admin"]))) -> Any:
    return await user_service.delete_user(user_id)


@router.patch("/{user_id}/role", response_model=UserResponse)
async def update_role(
    user_id: str,
    role: UserRole,
    _=Depends(require_roles(["admin"])),
) -> Any:
    update_data = UpdateUserRequest(role=role)
    return await user_service.update_user(user_id, update_data)
