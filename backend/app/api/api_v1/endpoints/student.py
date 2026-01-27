from typing import List
from fastapi import APIRouter, HTTPException, Query, UploadFile, File, Form, Query
from app.schemas.student import StudentResponse, StudentListResponse
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


@router.get("/", response_model=StudentListResponse)
async def list_students(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
):
    return await student_service.list_students(page=page, limit=limit)
