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
from app.models.ai_recommendation import (
    AIRecommendation,
)
from app.models.employee_risk import EmployeeRisk
from app.models.user import User
from app.schemas.ai_recommendation import (
    AIRecommendationCreate,
    AIRecommendationResponse,
    AIRecommendationUpdate,
)
from app.services.recommendation_service import (
    generate_recommendation,
)


router = APIRouter(
    prefix="/ai-recommendations",
    tags=["AI Recommendation Engine"],
)


@router.post(
    "/generate/{employee_id}",
    response_model=AIRecommendationResponse,
)
def generate_employee_recommendation(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "ADMIN",
            "HR",
            "MANAGER",
        )
    ),
):
    try:
        return generate_recommendation(
            db=db,
            employee_id=employee_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post(
    "",
    response_model=AIRecommendationResponse,
)
def create_recommendation(
    data: AIRecommendationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "ADMIN",
            "HR",
            "MANAGER",
        )
    ),
):
    risk = (
        db.query(EmployeeRisk)
        .filter(
            EmployeeRisk.employee_id
            == data.employee_id
        )
        .first()
    )

    if not risk:
        raise HTTPException(
            status_code=400,
            detail="Employee risk data not found",
        )

    recommendation = AIRecommendation(
        employee_id=data.employee_id,
        recommendation_type=(
            data.recommendation_type
        ),
        risk_level=risk.risk_level,
        recommendation=data.recommendation,
        priority=data.priority.upper(),
        status="PENDING",
        generated_by="manual",
    )

    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)

    return recommendation


@router.get(
    "",
    response_model=list[AIRecommendationResponse],
)
def list_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return (
        db.query(AIRecommendation)
        .order_by(
            AIRecommendation.created_at.desc()
        )
        .all()
    )


@router.get(
    "/employee/{employee_id}",
    response_model=list[AIRecommendationResponse],
)
def employee_recommendations(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    return (
        db.query(AIRecommendation)
        .filter(
            AIRecommendation.employee_id
            == employee_id
        )
        .order_by(
            AIRecommendation.created_at.desc()
        )
        .all()
    )


@router.get(
    "/{recommendation_id}",
    response_model=AIRecommendationResponse,
)
def get_recommendation(
    recommendation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    recommendation = (
        db.query(AIRecommendation)
        .filter(
            AIRecommendation.id
            == recommendation_id
        )
        .first()
    )

    if not recommendation:
        raise HTTPException(
            status_code=404,
            detail="Recommendation not found",
        )

    return recommendation


@router.put(
    "/{recommendation_id}",
    response_model=AIRecommendationResponse,
)
def update_recommendation(
    recommendation_id: int,
    data: AIRecommendationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "ADMIN",
            "HR",
            "MANAGER",
        )
    ),
):
    recommendation = (
        db.query(AIRecommendation)
        .filter(
            AIRecommendation.id
            == recommendation_id
        )
        .first()
    )

    if not recommendation:
        raise HTTPException(
            status_code=404,
            detail="Recommendation not found",
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    if "priority" in update_data:
        update_data["priority"] = (
            update_data["priority"].upper()
        )

    if "status" in update_data:
        update_data["status"] = (
            update_data["status"].upper()
        )

    for field, value in update_data.items():
        setattr(
            recommendation,
            field,
            value,
        )

    db.commit()
    db.refresh(recommendation)

    return recommendation


@router.delete(
    "/{recommendation_id}"
)
def delete_recommendation(
    recommendation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(
            "ADMIN",
            "HR",
        )
    ),
):
    recommendation = (
        db.query(AIRecommendation)
        .filter(
            AIRecommendation.id
            == recommendation_id
        )
        .first()
    )

    if not recommendation:
        raise HTTPException(
            status_code=404,
            detail="Recommendation not found",
        )

    db.delete(recommendation)
    db.commit()

    return {
        "message": (
            "AI recommendation deleted successfully"
        )
    }