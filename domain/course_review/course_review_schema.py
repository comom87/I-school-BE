# schema: api 명세서를 가지고 필요한 재료들을 채워넣는 것

import datetime

from pydantic import BaseModel, field_validator
from sqlalchemy import UUID

class CourseReview(BaseModel):
    courseId: int
    rating: float
    content: str

class CourseReviews(BaseModel):
    courseName: str
    courseReviews: list[CourseReview]

class CourseReview(BaseModel):
    userId: UUID
    courseId: int
    rating: int
    content: str