import uuid

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    nickname = Column(String, nullable=False)
    university = Column(String, nullable=False)
    major = Column(String, nullable=False)
    entrance_year = Column(Integer, nullable=False)
    certification = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)

    course_review = relationship("Course_Review", back_populates="user")
    timetable = relationship("Timetable", back_populates="user")

class Course_Review(Base):
    __tablename__ = "course_review"

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    content = Column(String, nullable=False)

    user = relationship("User", back_populates="course_review")
    course = relationship("Course", back_populates="course_review")

class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    professor = Column(String, nullable=False)
    major = Column(String, nullable=False)
    grade = Column(Integer, nullable=False)
    credit = Column(Integer, nullable=False)
    day = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    course_room = Column(String, nullable=False)

    course_review = relationship("Course_Review", back_populates="course")
    course_timetable = relationship("Course_Timetable", back_populates="course")

class Timetable(Base):
    __tablename__ = "timetable"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    name = Column(String, nullable=False)

    user = relationship("User", back_populates="timetable")
    course_timetable = relationship("Course_Timetable", back_populates="timetable")

class Course_Timetable(Base):
    __tablename__ = "course_timetable"

    id = Column(Integer, primary_key=True)
    timetable_id = Column(Integer, ForeignKey("timetable.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)

    timetable = relationship("Timetable", back_populates="course_timetable")
    course = relationship("Course", back_populates="course_timetable")