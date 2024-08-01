from typing import Annotated

from fastapi import Body

from models import Timetable, CourseTimetable, Course
from domain.timetable import timetable_schema
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from utils import UvicornException
from sqlalchemy.exc import SQLAlchemyError


def read_course_to_timetable(timetable_id: int, db: Session):
    # timetable = db.query(Timetable).filter(Timetable.id == timetable_id).first()
    # if not timetable:
    #     raise UvicornException(status_code=400, message="시간표가 존재하지 않습니다.")
    #
    # courses = db.query(
    #     func.array_agg(Course.id).label('id'),
    #     Course.code,
    #     Course.name,
    #     Course.professor,
    #     Course.major,
    #     func.array_agg(Course.day).label('day'),
    #     func.array_agg(Course.start_time).label('start_time'),
    #     func.array_agg(Course.end_time).label('end_time'),
    #     Course.course_room,
    # ).join(
    #     CourseTimetable, CourseTimetable.course_id == Course.id
    # ).filter(
    #     CourseTimetable.timetable_id == timetable_id
    # ).group_by(
    #     Course.code,
    #     Course.name,
    #     Course.professor,
    #     Course.major,
    #     Course.course_room
    # ).all()
    #
    # data = timetable_schema.CourseTimetableResponse(
    #     timetable_name=timetable.name,
    #     courses=[timetable_schema.CourseResponse(
    #         course_id=course.id,
    #         course_code=course.code,
    #         course_name=course.name,
    #         professor=course.professor,
    #         major=course.major,
    #         course_room=course.course_room,
    #         course_day=course.day,
    #         course_start_time=course.start_time,
    #         course_end_time=course.end_time
    #     ) for course in courses]
    # )
    # return data

    timetable = db.query(Timetable).filter(Timetable.id == timetable_id).first()
    if not timetable:
        raise UvicornException(status_code=400, message="시간표가 존재하지 않습니다.")

    course_timetables = db.query(CourseTimetable).filter(CourseTimetable.timetable_id == timetable_id).all()
    courses = []
    for course_timetable in course_timetables:
        course = db.query(Course).filter(Course.id == course_timetable.course_id).first()
        courses.append(course)

    data = timetable_schema.CourseTimetableResponse(
        timetable_name=timetable.name,
        courses=[timetable_schema.CourseResponse(
            course_id=course.id,
            course_code=course.code,
            course_name=course.name,
            professor=course.professor,
            major=course.major,
            course_room=course.course_room,
            course_day=course.day,
            course_start_time=course.start_time,
            course_end_time=course.end_time
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
        
        check = db.query(CourseTimetable).filter(
            and_(
                CourseTimetable.timetable_id == timetable_id,
                CourseTimetable.course_id == course.id
            )
        ).all()

        if check:
            raise UvicornException(status_code=400, message="이미 존재하는 강의입니다.")

        new_course = CourseTimetable(
            timetable_id=timetable_id,
            course_id=course.id
        )
        try :
            db.add(new_course)
            db.commit()
        except SQLAlchemyError as e:
            raise UvicornException(status_code=400, message="강의 추가중 오류 발생.")
            


def delete_course_from_timetable(timetable_id: int, request: timetable_schema.CourseRequest, db: Session):
    timetable = db.query(Timetable).filter(Timetable.id == timetable_id).first()
    if not timetable:
        raise UvicornException(status_code=400, message="시간표가 존재하지 않습니다.")

    courses = db.query(Course).filter(Course.code == request.course_code).all()
    if not courses:
        raise UvicornException(status_code=400, message="강의가 존재하지 않습니다.")

    for course in courses:
        course_timetable = db.query(CourseTimetable).filter(
            and_(CourseTimetable.timetable_id == timetable_id, 
                 CourseTimetable.course_id == course.id)).first()
        
        try :
            db.delete(course_timetable)
            db.commit()

        except SQLAlchemyError as e:
            raise UvicornException(status_code=400, message="강의 삭제중 오류 발생.")
    
