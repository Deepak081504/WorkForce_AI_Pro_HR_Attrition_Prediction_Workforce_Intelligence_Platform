from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.models.audit_log import AuditLog
from app.models.user import User
from app.schemas.audit_log import AuditLogResponse


router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs & Activity Tracking"],
)


@router.get(
    "",
    response_model=list[AuditLogResponse],
)
def list_audit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR")
    ),
):
    return (
        db.query(AuditLog)
        .order_by(
            AuditLog.created_at.desc()
        )
        .all()
    )


@router.get(
    "/user/{user_id}",
    response_model=list[AuditLogResponse],
)
def get_user_audit_logs(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR")
    ),
):
    return (
        db.query(AuditLog)
        .filter(
            AuditLog.user_id == user_id
        )
        .order_by(
            AuditLog.created_at.desc()
        )
        .all()
    )


@router.get(
    "/resource/{resource_type}/{resource_id}",
    response_model=list[AuditLogResponse],
)
def get_resource_audit_logs(
    resource_type: str,
    resource_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR")
    ),
):
    return (
        db.query(AuditLog)
        .filter(
            AuditLog.resource_type
            == resource_type,
            AuditLog.resource_id
            == resource_id,
        )
        .order_by(
            AuditLog.created_at.desc()
        )
        .all()
    )