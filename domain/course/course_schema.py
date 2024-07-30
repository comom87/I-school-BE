import datetime

from pydantic import BaseModel
from typing import Optional


class CourseResponse(BaseModel):
    course_id: list[int]
    course_code: str
    course_name: str
    professor: str
    grade: int
    credit: int
    course_day: list[str]
    course_start_time: list[datetime.time]
    course_end_time: list[datetime.time]
    course_room: str
    rating: float


class CoursesResponse(BaseModel):
    courses: list[CourseResponse]
