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
    university = Column(Enum('Uni1', 'Uni2', 'Uni3', name='university_enum'), nullable=False)
    major = Column(Enum('Major1', 'Major2', 'Major3', name='major_enum'), nullable=False)
    entrance_year = Column(Integer, nullable=False)
    certification = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)

    course_review = relationship("Course_Review", back_populates="users")
    timetable = relationship("Timetable", back_populates="users")

class Course_Review(Base):
    __tablename__ = "course_review"

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    content = Column(String, nullable=False)

    user = relationship("User", back_populates="course_reviews")
    course = relationship("Course", back_populates="course_reviews")

class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    professor = Column(String, nullable=False)
    major = Column(Enum('Major1', 'Major2', 'Major3', name='major_enum'), nullable=False)
    grade = Column(Integer, nullable=False)
    credit = Column(Integer, nullable=False)
    day = Column(Enum('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', name='day_enum'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    course_room = Column(String, nullable=False)

    course_review = relationship("Course_Review", back_populates="courses")
    course_timetable = relationship("Course_Timetable", back_populates="courses")

class Timetable(Base):
    __tablename__ = "timetable"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    name = Column(String, nullable=False)

    user = relationship("User", back_populates="timetables")
    course_timetable = relationship("Course_Timetable", back_populates="timetables")

class Course_Timetable(Base):
    __tablename__ = "course_timetable"

    id = Column(Integer, primary_key=True)
    timetable_id = Column(Integer, ForeignKey("timetable.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)

    timetable = relationship("Timetable", back_populates="course_timetables")
    course = relationship("Course", back_populates="course_timetables")