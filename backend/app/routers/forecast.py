from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
)
from app.models.user import User
from app.models.workforce_forecast import (
    WorkforceForecast,
)
from app.schemas.forecast import (
    WorkforceForecastRequest,
    WorkforceForecastResponse,
    WorkforceForecastItem,
)
from app.services.forecast_service import (
    generate_forecast,
)


router = APIRouter(
    prefix="/forecast",
    tags=["Workforce Forecasting"],
)


@router.post(
    "/workforce",
    response_model=WorkforceForecastResponse,
)
def workforce_forecast(
    data: WorkforceForecastRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    try:
        forecasts = generate_forecast(
            db=db,
            data=data,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    return WorkforceForecastResponse(
        message="Workforce forecast generated successfully",
        forecasts=[
            WorkforceForecastItem(**item)
            for item in forecasts
        ],
    )


@router.get(
    "",
    response_model=list[WorkforceForecastItem],
)
def list_forecasts(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    forecasts = (
        db.query(WorkforceForecast)
        .order_by(
            WorkforceForecast.forecast_period.asc()
        )
        .all()
    )

    return forecasts


@router.delete("/{forecast_id}")
def delete_forecast(
    forecast_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    forecast = (
        db.query(WorkforceForecast)
        .filter(
            WorkforceForecast.id == forecast_id
        )
        .first()
    )

    if not forecast:
        raise HTTPException(
            status_code=404,
            detail="Forecast not found",
        )

    db.delete(forecast)
    db.commit()

    return {
        "message": "Forecast deleted successfully"
    }