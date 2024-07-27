from typing import Optional, Any

from fastapi import FastAPI, Query, Body, Request
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from models import *
from domain.timetable import timetable_schema
from database import SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, or_

from domain.timetable import timetable_router
from utils import UvicornException, http_exception_handler

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


app.include_router(timetable_router.router)

app.add_exception_handler(UvicornException, http_exception_handler)

session = SessionLocal()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello_name(name: str):
    return {"message": f"Hello {name}"}
