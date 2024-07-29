from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_, func
from models import Course, CourseReview
from utils import UvicornException
from domain.course import course_schema


def read_courses(major: str, keyword: str, grade: str, db:Session):
    # 먼저 전공, 키워드, grade를 확인
    query = db.query(Course)
        
    # major 조건 추가
    if major:
        query = query.filter(Course.major == major)
        
    # grade 조건 추가
    if grade:
        query = query.filter(Course.grade == grade)
        
        # keyword 조건 추가
    if keyword:
        query = query.filter(
                or_(
                    Course.professor.ilike(f"%{keyword}%"),
                    Course.name.ilike(f"%{keyword}%")
                )
            )

    # 쿼리 실행
    courses = query.all()

        # 오류 메시지 반환
    if not courses:
        raise UvicornException(status_code=400, message="강의가 존재하지 않습니다.")

    # 서브쿼리: 별점 평점
    subquery = db.query(
        Course.id.label('course_id'),
        func.avg(CourseReview.rating).label('avg_rating')
    ).join(CourseReview, Course.id == CourseReview.course_id, isouter=True).group_by(
        Course.id
    ).subquery()

        # 메인 쿼리: Course와 서브쿼리 조인
    results = db.query(
        Course,
        subquery.c.avg_rating.label('review_rating')
    ).outerjoin(subquery, Course.id == subquery.c.course_id).filter(
        (Course.major == major if major else True),
        (Course.grade == grade if grade else True),
        (or_(Course.professor == keyword, Course.name == keyword) if keyword else True)
    ).order_by(
        Course.id  # 수업을 ID로 정렬
    ).all()

        # 데이터 변환
    course_dict = {}
    for course, avg_rating in results:
        if course.id not in course_dict:
            course_dict[course.id] = {
                "courseCode": course.code,
                "courseName": course.name,
                "professor": course.professor,
                "rating": avg_rating,
                "grade": course.grade,
                "credit": course.credit,
                "courseDay": [course.day],
                "courseStartTime": [course.start_time],
                "courseEndTime": [course.end_time],
                "courseRoom": course.course_room
            }
        else:
            course_dict[course.id]["courseDay"].append(course.day)
            course_dict[course.id]["courseStartTime"].append(course.start_time)
            course_dict[course.id]["courseEndTime"].append(course.end_time)


    course_list = list(course_dict.values())

    return {
            "success": True,
            "data": {
                "courses": course_list
            },
            "error": None
        }