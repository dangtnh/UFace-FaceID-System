from prisma import Prisma
from typing import List, Optional


class StudentRepository:
    def __init__(self):
        self.db = Prisma()

    async def connect(self):
        if not self.db.is_connected():
            await self.db.connect()

    async def find_by_id_or_email(self, student_id: str, email: str):
        await self.connect()
        return await self.db.student.find_first(
            where={"OR": [{"studentId": student_id}, {"schoolEmail": email}]}
        )

    async def create(self, data: dict):
        await self.connect()
        return await self.db.student.create(data=data)

    async def get_all(self, skip: int = 0, take: int = 100):
        await self.connect()
        return await self.db.student.find_many(skip=skip, take=take)

    async def delete(self, student_id: str):
        await self.connect()
        # Cần xử lý try/except nếu user không tồn tại
        return await self.db.student.delete(where={"studentId": student_id})


student_repo = StudentRepository()
