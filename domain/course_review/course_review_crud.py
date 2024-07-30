from sqlalchemy import and_, func

from models import Timetable, CourseTimetable, Course, CourseReview, User
from domain.course_review import course_review_schema
from sqlalchemy.orm import Session

from utils import UvicornException
from models import CourseReview


# /api/v1/course-reviews/?course-name={course_name}&professor={professor}

def read_course_reviews(course_name: str, professor: str, db: Session):
    # 1. course_name, prof 를 통해 course를 찾는다
    courses = db.query(Course).filter(and_(Course.name == course_name, Course.professor == professor)).all()
    if not courses:
        raise UvicornException(status_code=400, message="강의 목록이 존재하지 않습니다.")

    # [<object 'Course'>, ...]
    total_course_reviews = []
    for course in courses:
        course_reviews = db.query(CourseReview).filter(CourseReview.course_id == course.id).all()
        total_course_reviews += course_reviews

    data = course_review_schema.CourseReviewsResponse(
        course_name=courses[0].name,
        course_reviews=[course_review_schema.CourseReviewResponse(
            course_id=course_review.course_id,
            rating=course_review.rating,
            content=course_review.content
        ) for course_review in total_course_reviews]
    )
    return data


def create_course_reviews(request: course_review_schema.CourseReviewRequest, db: Session):
    user = db.query(User).filter(User.id == "11111111-1111-1111-1111-111111111111").first()
    if not user:
        raise UvicornException(status_code=400, message="사용자가 존재하지 않습니다.")

    course = db.query(Course).filter(Course.id == request.course_id).first()
    if not course:
        raise UvicornException(status_code=400, message="강의가 존재하지 않습니다.")

    new_review = CourseReview(
        user=user,
        course=course,
        rating=request.rating,
        content=request.content,
    )

    db.add(new_review)
    db.commit()

    average_rating = db.query(func.avg(CourseReview.rating)).join(Course, Course.id == CourseReview.course_id).filter(Course.code == course.code).scalar()

    courses = db.query(Course).filter(Course.code == course.code).all()
    for course in courses:
        course.rating = average_rating
        db.add(course)
        db.commit()