from fastapi import APIRouter

# KHAI BÁO BIẾN ROUTER (Đây là cái mà router.py đang tìm kiếm)
router = APIRouter()


@router.post("/login")
def login():
    """API Login giữ chỗ (Placeholder)"""
    return {"message": "Login successful (Demo)"}
