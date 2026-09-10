from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    require_roles,
)
from app.models.employee import Employee
from app.models.hr_intervention import HRIntervention
from app.models.user import User
from app.schemas.intervention import (
    InterventionCreate,
    InterventionResponse,
    InterventionUpdate,
)
from app.models.employee_risk import EmployeeRisk
from app.services.intervention_service import (
    create_intervention,
)


router = APIRouter(
    prefix="/interventions",
    tags=["HR Intervention & Decision Support"],
)


@router.post(
    "/generate/{employee_id}",
    response_model=InterventionResponse,
    status_code=status.HTTP_201_CREATED,
)
def generate_employee_intervention(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR", "MANAGER")
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

    try:
        return create_intervention(
            db=db,
            employee_id=employee_id,
            created_by=current_user.id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post(
    "",
    response_model=InterventionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_custom_intervention(
    data: InterventionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR", "MANAGER")
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
            detail="Risk information not available",
        )

    intervention = HRIntervention(
        employee_id=data.employee_id,
        risk_level=risk.risk_level,
        intervention_type=data.intervention_type.upper(),
        recommendation=data.recommendation,
        priority=data.priority.upper(),
        notes=data.notes,
        status="PENDING",
        created_by=current_user.id,
    )

    db.add(intervention)
    db.commit()
    db.refresh(intervention)

    return intervention


@router.get(
    "",
    response_model=list[InterventionResponse],
)
def list_interventions(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR", "MANAGER")
    ),
):
    return (
        db.query(HRIntervention)
        .order_by(
            HRIntervention.created_at.desc()
        )
        .all()
    )


@router.get(
    "/employee/{employee_id}",
    response_model=list[InterventionResponse],
)
def employee_interventions(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR", "MANAGER")
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
        db.query(HRIntervention)
        .filter(
            HRIntervention.employee_id
            == employee_id
        )
        .order_by(
            HRIntervention.created_at.desc()
        )
        .all()
    )


@router.get(
    "/{intervention_id}",
    response_model=InterventionResponse,
)
def get_intervention(
    intervention_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR", "MANAGER")
    ),
):
    intervention = (
        db.query(HRIntervention)
        .filter(
            HRIntervention.id
            == intervention_id
        )
        .first()
    )

    if not intervention:
        raise HTTPException(
            status_code=404,
            detail="Intervention not found",
        )

    return intervention


@router.put(
    "/{intervention_id}",
    response_model=InterventionResponse,
)
def update_intervention(
    intervention_id: int,
    data: InterventionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR", "MANAGER")
    ),
):
    intervention = (
        db.query(HRIntervention)
        .filter(
            HRIntervention.id
            == intervention_id
        )
        .first()
    )

    if not intervention:
        raise HTTPException(
            status_code=404,
            detail="Intervention not found",
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():

        if field in {
            "priority",
            "status",
        } and value:
            value = value.upper()

        setattr(
            intervention,
            field,
            value,
        )

    db.commit()
    db.refresh(intervention)

    return intervention


@router.delete(
    "/{intervention_id}"
)
def delete_intervention(
    intervention_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR")
    ),
):
    intervention = (
        db.query(HRIntervention)
        .filter(
            HRIntervention.id
            == intervention_id
        )
        .first()
    )

    if not intervention:
        raise HTTPException(
            status_code=404,
            detail="Intervention not found",
        )

    db.delete(intervention)
    db.commit()

    return {
        "message": "Intervention deleted successfully"
    }