from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EmployeeRiskResponse(BaseModel):
    id: int
    employee_id: int
    risk_score: float
    risk_level: str
    risk_reason: str | None
    last_prediction_id: int | None
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class RiskSummary(BaseModel):
    total_monitored: int
    high_risk: int
    medium_risk: int
    low_risk: int