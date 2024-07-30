from fastapi import FastAPI
from database import SessionLocal
from fastapi.middleware.cors import CORSMiddleware

from domain.timetable import timetable_router
from utils import UvicornException, http_exception_handler

from domain.course_review import course_review_router
from domain.course import course_router

app = FastAPI()

origins = [
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(course_router.router)
app.include_router(timetable_router.router)
app.include_router(course_review_router.router)

app.add_exception_handler(UvicornException, http_exception_handler)

session = SessionLocal()
