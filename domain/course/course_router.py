from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from utils import Response

from domain.course import course_crud

router = APIRouter(
    prefix="/api/v1"
)


@router.get("/courses", response_model=Response)
def get_courses(major: str | None = None, keyword: str | None = None, grade: int | None = None, db: Session = Depends(get_db)):
    courses = course_crud.read_courses(major, keyword, grade, db)
    return Response(success=True, data=courses, error=None)
