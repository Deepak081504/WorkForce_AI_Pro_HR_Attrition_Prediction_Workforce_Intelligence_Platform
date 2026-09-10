from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    require_roles,
)
from app.models.employee import Employee
from app.models.employee_risk import EmployeeRisk
from app.models.user import User
from app.schemas.risk import (
    EmployeeRiskResponse,
    RiskSummary,
)


router = APIRouter(
    prefix="/risk",
    tags=["Employee Risk Monitoring"],
)


@router.get(
    "/summary",
    response_model=RiskSummary,
)
def risk_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR")
    ),
):
    total_monitored = (
        db.query(EmployeeRisk)
        .count()
    )

    high_risk = (
        db.query(EmployeeRisk)
        .filter(
            EmployeeRisk.risk_level == "HIGH"
        )
        .count()
    )

    medium_risk = (
        db.query(EmployeeRisk)
        .filter(
            EmployeeRisk.risk_level == "MEDIUM"
        )
        .count()
    )

    low_risk = (
        db.query(EmployeeRisk)
        .filter(
            EmployeeRisk.risk_level == "LOW"
        )
        .count()
    )

    return RiskSummary(
        total_monitored=total_monitored,
        high_risk=high_risk,
        medium_risk=medium_risk,
        low_risk=low_risk,
    )


@router.get(
    "",
    response_model=list[EmployeeRiskResponse],
)
def list_employee_risks(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR", "MANAGER")
    ),
):
    return (
        db.query(EmployeeRisk)
        .order_by(
            EmployeeRisk.risk_score.desc()
        )
        .all()
    )


@router.get(
    "/high",
    response_model=list[EmployeeRiskResponse],
)
def high_risk_employees(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR", "MANAGER")
    ),
):
    return (
        db.query(EmployeeRisk)
        .filter(
            EmployeeRisk.risk_level == "HIGH"
        )
        .order_by(
            EmployeeRisk.risk_score.desc()
        )
        .all()
    )


@router.get(
    "/medium",
    response_model=list[EmployeeRiskResponse],
)
def medium_risk_employees(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR", "MANAGER")
    ),
):
    return (
        db.query(EmployeeRisk)
        .filter(
            EmployeeRisk.risk_level == "MEDIUM"
        )
        .order_by(
            EmployeeRisk.risk_score.desc()
        )
        .all()
    )


@router.get(
    "/employee/{employee_id}",
    response_model=EmployeeRiskResponse,
)
def employee_risk(
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

    risk = (
        db.query(EmployeeRisk)
        .filter(
            EmployeeRisk.employee_id
            == employee_id
        )
        .first()
    )

    if not risk:
        raise HTTPException(
            status_code=404,
            detail=(
                "Risk information not available "
                "for this employee"
            ),
        )

    return risk