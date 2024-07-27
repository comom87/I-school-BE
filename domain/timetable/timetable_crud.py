from models import Timetable, CourseTimetable, Course
from domain.timetable import timetable_schema
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, or_

from utils import UvicornException


def read_course_timetable(timetable_id: int, db: Session):
    timetable = db.query(Timetable).filter(
        Timetable.id == timetable_id).first()
    if not timetable:
        raise UvicornException(status_code=400, message="시간표가 존재하지 않습니다.")
    course_timetables = db.query(CourseTimetable).filter(
        CourseTimetable.timetable_id == timetable_id).all()
    courses = []
    for course_timetable in course_timetables:
        course = db.query(Course).filter(
            Course.id == course_timetable.course_id).first()
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


def insert_course_to_timetable(timetable_id: int, userId: int, code: str, db: Session):

    course = db.query(Course.id).filter(Course.code == code).all()
    if not course:
        raise UvicornException(status_code=400, message="강의가 존재하지 않습니다.")

    timetable = db.query(Timetable).filter(
        Timetable.id == timetable_id).first()
    if not timetable:
        raise UvicornException(status_code=400, message="시간표가 존재하지 않습니다.")

    for courseId in course:
        courses = CourseTimetable()
        courses.timetable_id = timetable_id
        courses.course_id = courseId[0]

        try:
            db.add(courses)
            db.commit()
            db.refresh(courses)

        except SQLAlchemyError as e:
            db.rollback()
            print(f'강의 추가 에러 발생 \n {e}')
            raise UvicornException(status_code=400, message=f'강의 추가 에러 발생')

    return None

def delete_course_from_timetable(timetable_id: int, userId: int, code: str, db: Session):

    course = db.query(Course.id).filter(Course.code == code).all()
    if not course:
        raise UvicornException(status_code=400, message="강의가 존재하지 않습니다.")

    timetable = db.query(Timetable).filter(
        Timetable.id == timetable_id).first()
    if not timetable:
        raise UvicornException(status_code=400, message="시간표가 존재하지 않습니다.")

    for courseId in course:


        try:
            courseId[0]
            db.query(CourseTimetable).filter(and_(
                CourseTimetable.course_id == courseId[0],
                CourseTimetable.timetable_id == timetable_id)).delete()
            db.commit()

        except SQLAlchemyError as e:
            db.rollback()
            print(f'강의 삭제 에러 발생 \n {e}')
            raise UvicornException(status_code=400, message=f'강의 삭제 에러 발생')

    return None
