from models import Timetable, CourseTimetable, Course
from domain.timetable import timetable_schema
from sqlalchemy.orm import Session

from utils import UvicornException


def read_course_timetable(timetable_id: int, db: Session):
    timetable = db.query(Timetable).filter(Timetable.id == timetable_id).first()
    if not timetable:
        raise UvicornException(status_code=400, message="시간표가 존재하지 않습니다.")
    course_timetables = db.query(CourseTimetable).filter(CourseTimetable.timetable_id == timetable_id).all()
    courses = []
    for course_timetable in course_timetables:
        course = db.query(Course).filter(Course.id == course_timetable.course_id).first()
        courses.append(course)

    data = timetable_schema.CourseTimetable(
        timetableName=timetable.name,
        courses=[timetable_schema.Course(
            courseCode=course.code,
            courseName=course.name,
            courseRoom=course.course_room,
            courseDay=course.day,
            courseStartTime=course.start_time,
            courseEndTime=course.end_time
        ) for course in courses]
    )
    return data
