from typing import List, Dict, Any
from fastapi import UploadFile
from app.schemas.student import StudentCreate
from app.repositories.student import student_repo
from app.services.face import face_service


class StudentService:
    async def register_student(
        self,
        full_name: str,
        student_id: str,
        school_email: str,
        images: List[UploadFile],
    ):
        existing = await student_repo.find_by_id_or_email(student_id, school_email)
        if existing:
            raise Exception("Sinh viên đã tồn tại (Trùng ID hoặc Email)")

        new_student = await student_repo.create(
            data={
                "fullName": full_name,
                "studentId": student_id,
                "schoolEmail": school_email,
                "status": "active",
            }
        )

        if images:
            await face_service.register_student(
                mssv=new_student.studentId, name=new_student.fullName, files=images
            )

        return new_student

    async def list_students(self, page: int = 1, limit: int = 10) -> Dict[str, Any]:
        skip = (page - 1) * limit

        students = await student_repo.list_students(skip=skip, take=limit)

        total = await student_repo.count()

        return {
            "data": students,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "totalPages": (total + limit - 1) // limit if limit > 0 else 1,
            },
        }


student_service = StudentService()
