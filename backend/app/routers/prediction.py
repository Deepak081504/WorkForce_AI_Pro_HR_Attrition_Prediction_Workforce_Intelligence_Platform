from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    require_roles,
)
from app.models.attrition_prediction import (
    AttritionPrediction,
)
from app.models.employee import Employee
from app.models.user import User
from app.schemas.prediction import (
    AttritionPredictionRequest,
    AttritionPredictionResponse,
)
from app.services.attrition_service import (
    predict_attrition,
)


router = APIRouter(
    prefix="/predictions",
    tags=["AI Attrition Prediction"],
)


@router.post(
    "/attrition",
    response_model=AttritionPredictionResponse,
)
def predict_employee_attrition(
    data: AttritionPredictionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    employee = (
        db.query(Employee)
        .filter(
            Employee.id == data.employee_id
        )
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    try:
        return predict_attrition(
            db=db,
            data=data,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/employee/{employee_id}",
    response_model=list[
        AttritionPredictionResponse
    ],
)
def employee_predictions(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    employee = (
        db.query(Employee)
        .filter(
            Employee.id == employee_id
        )
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    return (
        db.query(AttritionPrediction)
        .filter(
            AttritionPrediction.employee_id
            == employee_id
        )
        .order_by(
            AttritionPrediction.predicted_at.desc()
        )
        .all()
    )


@router.get(
    "/high-risk",
    response_model=list[
        AttritionPredictionResponse
    ],
)
def high_risk_employees(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR")
    ),
):
    return (
        db.query(AttritionPrediction)
        .filter(
            AttritionPrediction.risk_level
            == "HIGH"
        )
        .order_by(
            AttritionPrediction.attrition_probability.desc()
        )
        .all()
    )