from datetime import datetime

from pydantic import BaseModel, Field


class AttritionPredictionRequest(BaseModel):
    employee_id: int

    age: float = Field(ge=18, le=100)

    monthly_income: float = Field(
        ge=0
    )

    years_at_company: float = Field(
        ge=0
    )

    years_in_current_role: float = Field(
        ge=0
    )

    job_satisfaction: float = Field(
        ge=1,
        le=5,
    )

    environment_satisfaction: float = Field(
        ge=1,
        le=5,
    )

    work_life_balance: float = Field(
        ge=1,
        le=5,
    )

    overtime: int = Field(
        ge=0,
        le=1,
    )

    job_level: float = Field(
        ge=1,
        le=5,
    )

    num_companies_worked: float = Field(
        ge=0
    )


class AttritionPredictionResponse(BaseModel):
    id: int
    employee_id: int
    attrition_probability: float
    risk_level: str
    model_version: str
    predicted_at: datetime

    class Config:
        from_attributes = True