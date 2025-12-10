from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from prisma import Prisma
from app.schemas.student import StudentResponse
from app.services.student_service import StudentService

router = APIRouter()


async def get_db():
    db = Prisma()
    await db.connect()
    try:
        yield db
    finally:
        await db.disconnect()


# --- API ĐĂNG KÝ SINH VIÊN (QUAN TRỌNG NHẤT) ---
@router.post("/register", response_model=StudentResponse)
async def register_student(
    fullName: str = Form(...),
    studentId: str = Form(...),
    schoolEmail: str = Form(...),
    # Nhận danh sách ảnh (List)
    face_images: List[UploadFile] = File(...),
    db: Prisma = Depends(get_db),
):
    try:
        service = StudentService(db)
        new_student = await service.register_student(
            full_name=fullName,
            student_id=studentId,
            school_email=schoolEmail,
            images=face_images,
        )
        return new_student

    except Exception as e:
        print(f"Lỗi đăng ký: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[StudentResponse])
async def list_student(skip: int = 0, take: int = 100, db: Prisma = Depends(get_db)):
    students = await db.student.find_many(skip=skip, take=take)
    return students


@router.delete("/{student_id}")
async def delete_student(student_id: str, db: Prisma = Depends(get_db)):
    # Logic xóa sẽ viết sau
    return {"message": f"Đã xóa sinh viên {student_id}"}
