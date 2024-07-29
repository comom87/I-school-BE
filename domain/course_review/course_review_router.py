# router는 전체적인 껍데기 ~

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from domain.course_review import course_review_schema, course_review_crud
from utils import Response

from models import CourseReview

router = APIRouter(
    prefix="/api/v1"
)

# url 값을 받으면 router에서 아래 함수를 받아오겠음
@router.get("/course-reviews/", response_model=Response)

# course_name과 professor를 query parameter로 받아서 함수 실행
# 참고: path parameter: / 뒤에 있는 것, query parameter: ? 뒤에 있는 것
# ?course-name={course_name}&professor={professor} 이 자동으로 뒤에 들어감
def get_course_reviews(course_name: str, professor: str, db: Session = Depends(get_db)):
    # course_review_crud에 있는 read_course_reviews 함수를 불러오겠다.
    course_reviews = course_review_crud.read_course_reviews(course_name, professor, db)
    # api 명세서 형식에 맞게 success, data(course_reviews), error를 return
    return Response(success=True, data=course_reviews, error=None)

@router.post("/course-reviews/")
# post라 request body로 받아야함
def post_course_review(request: course_review_schema.CourseReview, db: Session = Depends(get_db)):
    course_review_crud.create_course_reviews(request, db)
    return Response(success=True, data=None, error=None)