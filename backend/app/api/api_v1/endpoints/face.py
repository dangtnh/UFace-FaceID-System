from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
from app.services.face_service import face_service

router = APIRouter()


@router.post("/register")
async def register(
    mssv: str = Form(...), name: str = Form(...), files: List[UploadFile] = File(...)
):
    try:
        return await face_service.register_student(mssv, name, files)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/recognize")
async def check_in(file: UploadFile = File(...)):
    return await face_service.recognize_image(file)
