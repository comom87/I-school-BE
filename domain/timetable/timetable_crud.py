from typing import Annotated

from fastapi import Body

from models import Timetable, CourseTimetable, Course
from domain.timetable import timetable_schema
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_

from utils import UvicornException


def read_course_to_timetable(timetable_id: int, db: Session):
    timetable = db.query(Timetable).filter(Timetable.id == timetable_id).first()
    if not timetable:
        raise UvicornException(status_code=400, message="시간표가 존재하지 않습니다.")

    course_timetables = db.query(CourseTimetable).filter(CourseTimetable.timetable_id == timetable_id).all()
    courses = []
    for course_timetable in course_timetables:
        course = db.query(Course).filter(Course.id == course_timetable.course_id).first()
        courses.append(course)

    data = timetable_schema.CourseTimetableResponse(
        timetableName=timetable.name,
        courses=[timetable_schema.CourseResponse(
            courseCode=course.code,
            courseName=course.name,
            professor=course.professor,
            courseRoom=course.course_room,
            courseDay=course.day,
            courseStartTime=course.start_time,
            courseEndTime=course.end_time
        ) for course in courses]
    )
    return data


def create_course_to_timetable(timetable_id: int, request: timetable_schema.CourseRequest, db: Session):
    timetable = db.query(Timetable).filter(Timetable.id == timetable_id).first()
    if not timetable:
        raise UvicornException(status_code=400, message="시간표가 존재하지 않습니다.")

    courses = db.query(Course).filter(Course.code == request.course_code).all()
    if not courses:
        raise UvicornException(status_code=400, message="강의가 존재하지 않습니다.")

    for course in courses:
        new_course = CourseTimetable(
            timetable=timetable,
            course_id=course.id
        )
        db.add(new_course)
        db.commit()
    return None


def delete_course_from_timetable(timetable_id: int, request: timetable_schema.CourseRequest, db: Session):
    timetable = db.query(Timetable).filter(Timetable.id == timetable_id).first()
    if not timetable:
        raise UvicornException(status_code=400, message="시간표가 존재하지 않습니다.")

    courses = db.query(Course).filter(Course.code == request.course_code).all()
    if not courses:
        raise UvicornException(status_code=400, message="강의가 존재하지 않습니다.")

    for course in courses:
        course_timetable = db.query(CourseTimetable).filter(and_(CourseTimetable.timetable_id == timetable_id, CourseTimetable.course_id == course.id)).first()
        db.delete(course_timetable)
        db.commit()
    return None
