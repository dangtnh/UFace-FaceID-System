from typing import List, Optional
from app.core.database import prisma


class StudentRepository:
    async def find_by_id_or_email(self, student_id: str, email: str):
        return await prisma.student.find_first(
            where={"OR": [{"studentId": student_id}, {"schoolEmail": email}]}
        )

    async def create_student(self, data: dict):
        return await prisma.student.create(data=data)

    async def list_students(self, skip: int = 0, take: int = 100):
        return await prisma.student.find_many(skip=skip, take=take)

    async def count(self) -> int:
        return await prisma.student.count()

    async def delete(self, student_id: str):
        return await prisma.student.delete(where={"studentId": student_id})


student_repo = StudentRepository()
