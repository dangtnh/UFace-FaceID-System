from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Any


class StudentCreate(BaseModel):
    fullName: str
    studentId: str
    schoolEmail: EmailStr


class StudentResponse(BaseModel):
    id: int
    fullName: str
    studentId: str
    schoolEmail: str
    status: str
    createdAt: datetime

    class Config:
        from_attributes = True


class PaginationSchema(BaseModel):
    page: int
    limit: int
    total: int
    totalPages: int


class StudentListResponse(BaseModel):
    data: List[StudentResponse]
    pagination: PaginationSchema
