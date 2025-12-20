from typing import List
from fastapi import UploadFile
from app.schemas.student import StudentCreate
from app.repositories.student_repo import student_repo
from app.services.face_service import face_service


class StudentService:
    async def register_student(
        self,
        full_name: str,
        student_id: str,
        school_email: str,
        images: List[UploadFile],
    ):
        # 1. Gọi Repo kiểm tra trùng
        existing = await student_repo.find_by_id_or_email(student_id, school_email)
        if existing:
            raise Exception("Sinh viên đã tồn tại (Trùng ID hoặc Email)")

        # 2. Gọi Repo lưu DB
        new_student = await student_repo.create(
            data={
                "fullName": full_name,
                "studentId": student_id,
                "schoolEmail": school_email,
                "status": "active",
            }
        )

        # 3. Gọi AI Train
        if images:
            await face_service.register_student(
                mssv=new_student.studentId, name=new_student.fullName, files=images
            )

        return new_student

    async def get_all_students(self, skip: int, take: int):
        return await student_repo.get_all(skip, take)


student_service = StudentService()
