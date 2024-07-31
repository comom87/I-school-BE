import datetime

from pydantic import BaseModel, Field

class CourseResponse(BaseModel):
    # course_id: list[int]
    # course_code: str
    # course_name: str
    # professor: str
    # major: str
    # course_day: list[str]
    # course_start_time: list[datetime.time]
    # course_end_time: list[datetime.time]
    # course_room: str

    course_id: int
    course_code: str
    course_name: str
    professor: str
    major: str
    course_day: str
    course_start_time: datetime.time
    course_end_time: datetime.time
    course_room: str

class CourseTimetableResponse(BaseModel):
    timetable_name: str
    courses: list[CourseResponse]

class CourseRequest(BaseModel):
    course_code: str = Field(..., alias="courseCode")

    class Config:
        populate_by_name = True