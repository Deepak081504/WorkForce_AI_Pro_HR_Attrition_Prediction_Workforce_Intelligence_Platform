from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.models.user import User
from app.services.report_service import (
    create_csv,
    create_excel,
    get_attendance_report,
    get_attrition_risk_report,
    get_employee_report,
    get_leave_report,
    get_payroll_report,
)


router = APIRouter(
    prefix="/reports",
    tags=["Reports & Export"],
)


REPORT_FUNCTIONS = {
    "employees": get_employee_report,
    "attendance": get_attendance_report,
    "leaves": get_leave_report,
    "payroll": get_payroll_report,
    "attrition-risk": get_attrition_risk_report,
}


@router.get(
    "/{report_type}/csv"
)
def export_csv(
    report_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR")
    ),
):
    report_function = REPORT_FUNCTIONS.get(
        report_type
    )

    if not report_function:
        raise HTTPException(
            status_code=404,
            detail="Invalid report type",
        )

    data = report_function(db)

    output = create_csv(data)

    filename = f"{report_type}_report.csv"

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{filename}"'
            )
        },
    )


@router.get(
    "/{report_type}/excel"
)
def export_excel(
    report_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR")
    ),
):
    report_function = REPORT_FUNCTIONS.get(
        report_type
    )

    if not report_function:
        raise HTTPException(
            status_code=404,
            detail="Invalid report type",
        )

    data = report_function(db)

    output = create_excel(data)

    filename = f"{report_type}_report.xlsx"

    return StreamingResponse(
        output,
        media_type=(
            "application/vnd.openxmlformats-"
            "officedocument.spreadsheetml.sheet"
        ),
        headers={
            "Content-Disposition": (
                f'attachment; filename="{filename}"'
            )
        },
    )