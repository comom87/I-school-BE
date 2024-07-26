from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from domain.timetable import timetable_schema, timetable_crud
from utils import Response

router = APIRouter(
    prefix="/api/v1"
)


@router.get("/timetables/{timetable_id}", response_model=Response)
def get_course_timetables(timetable_id: int, db: Session = Depends(get_db)):
    course_timetables = timetable_crud.read_course_timetable(timetable_id, db)
    return Response(success=True, data=course_timetables, error=None)
