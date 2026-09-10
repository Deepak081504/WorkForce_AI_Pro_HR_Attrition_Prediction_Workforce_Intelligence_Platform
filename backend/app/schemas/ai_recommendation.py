from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AIRecommendationCreate(BaseModel):
    employee_id: int

    recommendation_type: str = Field(
        min_length=2,
        max_length=50,
    )

    recommendation: str = Field(
        min_length=5,
        max_length=3000,
    )

    priority: str = Field(
        default="MEDIUM",
        max_length=20,
    )


class AIRecommendationUpdate(BaseModel):
    priority: str | None = Field(
        default=None,
        max_length=20,
    )

    status: str | None = Field(
        default=None,
        max_length=30,
    )

    recommendation: str | None = Field(
        default=None,
        max_length=3000,
    )


class AIRecommendationResponse(BaseModel):
    id: int
    employee_id: int
    recommendation_type: str
    risk_level: str
    recommendation: str
    priority: str
    status: str
    generated_by: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )