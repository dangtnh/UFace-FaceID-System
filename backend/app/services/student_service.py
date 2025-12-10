from typing import List
from fastapi import UploadFile
from prisma import Prisma
from app.schemas.student import StudentCreate

# Import instance face_service từ file bên trên
from app.services.face_service import face_service


class StudentService:
    def __init__(self, db: Prisma):
        self.db = db

    async def register_student(
        self,
        full_name: str,
        student_id: str,
        school_email: str,
        images: List[UploadFile],
    ):
        # BƯỚC 1: Kiểm tra trùng lặp trong SQL
        existing = await self.db.student.find_first(
            where={"OR": [{"studentId": student_id}, {"schoolEmail": school_email}]}
        )
        if existing:
            raise Exception("Sinh viên đã tồn tại (Trùng ID hoặc Email)")

        # BƯỚC 2: Lưu vào PostgreSQL
        new_student = await self.db.student.create(
            data={
                "fullName": full_name,
                "studentId": student_id,
                "schoolEmail": school_email,
                "status": "active",
            }
        )

        # BƯỚC 3: Gọi FaceService để xử lý AI
        # Truyền đúng tham số mà hàm register_student của FaceService yêu cầu (mssv, name, files)
        if images:
            await face_service.register_student(
                mssv=new_student.studentId, name=new_student.fullName, files=images
            )

        return new_student
