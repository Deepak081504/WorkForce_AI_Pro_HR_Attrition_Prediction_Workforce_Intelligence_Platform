from pydantic import BaseModel


class AttritionOverview(BaseModel):
    total_predictions: int
    high_risk: int
    medium_risk: int
    low_risk: int
    average_attrition_probability: float


class RiskDistribution(BaseModel):
    risk_level: str
    employee_count: int


class DepartmentRiskAnalytics(BaseModel):
    department_id: int
    department_name: str
    employee_count: int
    high_risk_count: int
    average_risk_score: float


class AttritionAnalyticsResponse(BaseModel):
    overview: AttritionOverview
    risk_distribution: list[RiskDistribution]
    department_analysis: list[DepartmentRiskAnalytics]