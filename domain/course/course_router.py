from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from utils import Response
from . import course_crud , course_schema
router = APIRouter(
    prefix="/api/v1"
)

@router.get("/courses", response_model=Response)
async def read_courses(major: str | None = None, keyword: str | None = None, grade: int | None = None, db: Session = Depends(get_db)):
    courses = course_crud.read_courses(major, keyword, grade, db)
    return Response(success=True, data=courses, error=None)
