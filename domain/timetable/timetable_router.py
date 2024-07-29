from typing import Annotated

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from database import get_db
from domain.timetable import timetable_schema, timetable_crud
from utils import Response

router = APIRouter(
    prefix="/api/v1"
)


@router.get("/timetables/{timetable_id}", response_model=Response)
def get_course_timetables(timetable_id: int, db: Session = Depends(get_db)):
    course_timetables = timetable_crud.read_course_to_timetable(timetable_id, db)
    return Response(success=True, data=course_timetables, error=None)


@router.post("/timetables/{timetable_id}", response_model=Response)
def post_course_to_timetable(timetable_id: int, request: timetable_schema.CourseRequest, db: Session = Depends(get_db)):
    timetable_crud.create_course_to_timetable(timetable_id, request, db)
    return Response(success=True, data=None, error=None)


@router.delete("/timetables/{timetable_id}", response_model=Response)
def delete_course_from_timetable(timetable_id: int, request: timetable_schema.CourseRequest, db: Session = Depends(get_db)):
    timetable_crud.delete_course_from_timetable(timetable_id, request, db)
    return Response(success=True, data=None, error=None)
