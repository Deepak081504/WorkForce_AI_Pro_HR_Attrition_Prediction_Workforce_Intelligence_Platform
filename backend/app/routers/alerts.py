from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.models.user import User
from app.services.alert_service import (
    create_risk_alerts,
)


router = APIRouter(
    prefix="/alerts",
    tags=["Smart Notification & Alert Engine"],
)


@router.post(
    "/employee/{employee_id}"
)
def generate_employee_alert(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR")
    ),
):
    try:
        return create_risk_alerts(
            db=db,
            employee_id=employee_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )