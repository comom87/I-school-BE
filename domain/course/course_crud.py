from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from models import Course
from utils import UvicornException

from domain.course import course_schema


def read_courses(major: str, keyword: str, grade: int, db: Session):
    query = db.query(
        func.array_agg(Course.id).label('id'),
        Course.code,
        Course.name,
        Course.professor,
        Course.grade,
        Course.credit,
        func.array_agg(Course.day).label('day'),
        func.array_agg(Course.start_time).label('start_time'),
        func.array_agg(Course.end_time).label('end_time'),
        Course.course_room,
        Course.rating
    )

    # major 조건 추가
    if major:
        query = query.filter(Course.major == major)

    # keyword 조건 추가
    if keyword:
        query = query.filter(
            or_(
                Course.professor.ilike(f"%{keyword}%"),
                Course.name.ilike(f"%{keyword}%")
            )
        )

    # grade 조건 추가
    if grade:
        query = query.filter(Course.grade == grade)

    # 그룹화 및 쿼리 실행
    query = query.group_by(Course.code, Course.name, Course.professor, Course.grade, Course.credit, Course.course_room,
                           Course.rating)
    courses = query.all()

    # 오류 메시지 반환
    if not courses:
        raise UvicornException(status_code=400, message="강의가 존재하지 않습니다.")

    print(courses)

    # 데이터 변환
    data = course_schema.CoursesResponse(
        courses=[course_schema.CourseResponse(
            course_id=course.id,
            course_code=course.code,
            course_name=course.name,
            professor=course.professor,
            grade=course.grade,
            credit=course.credit,
            course_day=course.day,
            course_start_time=course.start_time,
            course_end_time=course.end_time,
            course_room=course.course_room,
            rating=course.rating
        ) for course in courses]
    )

    return data
