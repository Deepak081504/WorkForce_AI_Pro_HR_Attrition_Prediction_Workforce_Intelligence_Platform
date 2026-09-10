from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import (
    get_current_user,
    require_roles,
)
from app.models.shift import Shift
from app.models.user import User
from app.schemas.shift import (
    ShiftCreate,
    ShiftResponse,
    ShiftUpdate,
)

router = APIRouter(
    prefix="/shifts",
    tags=["Shift Management"],
)


@router.post(
    "",
    response_model=ShiftResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_shift(
    data: ShiftCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR")
    ),
):
    existing = (
        db.query(Shift)
        .filter(Shift.name == data.name)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Shift already exists",
        )

    if data.start_time == data.end_time:
        raise HTTPException(
            status_code=400,
            detail="Start time and end time cannot be the same",
        )

    shift = Shift(
        name=data.name,
        start_time=data.start_time,
        end_time=data.end_time,
        description=data.description,
    )

    db.add(shift)
    db.commit()
    db.refresh(shift)

    return shift


@router.get(
    "",
    response_model=list[ShiftResponse],
)
def list_shifts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Shift)
        .order_by(Shift.id.desc())
        .all()
    )


@router.get(
    "/{shift_id}",
    response_model=ShiftResponse,
)
def get_shift(
    shift_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    shift = (
        db.query(Shift)
        .filter(Shift.id == shift_id)
        .first()
    )

    if not shift:
        raise HTTPException(
            status_code=404,
            detail="Shift not found",
        )

    return shift


@router.put(
    "/{shift_id}",
    response_model=ShiftResponse,
)
def update_shift(
    shift_id: int,
    data: ShiftUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR")
    ),
):
    shift = (
        db.query(Shift)
        .filter(Shift.id == shift_id)
        .first()
    )

    if not shift:
        raise HTTPException(
            status_code=404,
            detail="Shift not found",
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    if "name" in update_data:
        existing = (
            db.query(Shift)
            .filter(
                Shift.name == update_data["name"],
                Shift.id != shift_id,
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Shift name already exists",
            )

    for field, value in update_data.items():
        setattr(shift, field, value)

    db.commit()
    db.refresh(shift)

    return shift


@router.delete("/{shift_id}")
def delete_shift(
    shift_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR")
    ),
):
    shift = (
        db.query(Shift)
        .filter(Shift.id == shift_id)
        .first()
    )

    if not shift:
        raise HTTPException(
            status_code=404,
            detail="Shift not found",
        )

    db.delete(shift)
    db.commit()

    return {
        "message": "Shift deleted successfully"
    }