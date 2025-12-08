from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_students():
    """API Student giữ chỗ"""
    return [{"id": 1, "name": "Student A"}]
