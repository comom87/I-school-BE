from pydantic import BaseModel, Field


class CourseReviewResponse(BaseModel):
    course_id: int
    rating: float
    content: str


class CourseReviewsResponse(BaseModel):
    course_name: str
    course_reviews: list[CourseReviewResponse]


class CourseReviewRequest(BaseModel):
    course_id: int = Field(..., alias="courseId")
    rating: int = Field(..., alias="rating")
    content: str = Field(..., alias="content")

    class Config:
        populate_by_name = True
