import datetime

from pydantic import BaseModel, Field


class Course(BaseModel):
    courseCode: str
    courseName: str
    courseRoom: str
    courseDay: str
    courseStartTime: datetime.time
    courseEndTime: datetime.time

class CourseTimetable(BaseModel):
    timetableName: str
    courses: list[Course]
