from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class PerformanceReviewCreate(BaseModel):
    employee_id: int

    review_period: str = Field(
        min_length=3,
        max_length=30,
    )

    rating: float | None = Field(
        default=None,
        ge=1,
        le=5,
    )

    strengths: str | None = Field(
        default=None,
        max_length=3000,
    )

    areas_for_improvement: str | None = Field(
        default=None,
        max_length=3000,
    )

    goals: str | None = Field(
        default=None,
        max_length=3000,
    )

    feedback: str | None = Field(
        default=None,
        max_length=3000,
    )


class PerformanceReviewUpdate(BaseModel):
    rating: float | None = Field(
        default=None,
        ge=1,
        le=5,
    )

    strengths: str | None = Field(
        default=None,
        max_length=3000,
    )

    areas_for_improvement: str | None = Field(
        default=None,
        max_length=3000,
    )

    goals: str | None = Field(
        default=None,
        max_length=3000,
    )

    feedback: str | None = Field(
        default=None,
        max_length=3000,
    )

    status: str | None = Field(
        default=None,
        max_length=30,
    )


class PerformanceReviewResponse(BaseModel):
    id: int
    employee_id: int
    reviewer_id: int
    review_period: str
    rating: float | None
    strengths: str | None
    areas_for_improvement: str | None
    goals: str | None
    feedback: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )