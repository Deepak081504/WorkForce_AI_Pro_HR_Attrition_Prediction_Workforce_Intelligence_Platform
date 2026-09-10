from pydantic import BaseModel, Field


class ForecastDataPoint(BaseModel):
    period: str = Field(
        min_length=3,
        max_length=20,
    )

    headcount: int = Field(
        ge=0,
    )


class WorkforceForecastRequest(BaseModel):
    historical_data: list[ForecastDataPoint]

    periods_to_forecast: int = Field(
        default=3,
        ge=1,
        le=24,
    )


class WorkforceForecastItem(BaseModel):
    forecast_period: str
    predicted_headcount: float
    model_version: str


class WorkforceForecastResponse(BaseModel):
    message: str
    forecasts: list[WorkforceForecastItem]