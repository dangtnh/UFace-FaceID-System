from typing import List
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.schemas.student import StudentResponse
from app.services.student import student_service

router = APIRouter()


@router.post("/register", response_model=StudentResponse)
async def register_student(
    fullName: str = Form(...),
    studentId: str = Form(...),
    schoolEmail: str = Form(...),
    face_images: List[UploadFile] = File(...),
):
    try:
        return await student_service.register_student(
            full_name=fullName,
            student_id=studentId,
            school_email=schoolEmail,
            images=face_images,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[StudentResponse])
async def list_student(skip: int = 0, take: int = 100):
    return await student_service.get_all_students(skip, take)
