from pydantic import BaseModel
from typing import List, Optional

class Course(BaseModel):
    courseCode: str
    courseName: str
    professor: str
    grade: int
    credit: int
    courseDay: list[str]
    courseStartTime: list[str]
    courseEndTime: list[str]
    courseRoom: str
    rating: Optional[float]

class Courses(BaseModel):
    success: bool
    data: Optional[List[Course]]
    error: Optional[str]
