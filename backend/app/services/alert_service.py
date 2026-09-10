from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.employee_risk import EmployeeRisk
from app.models.notification import Notification
from app.models.user import User


def create_risk_alerts(
    db: Session,
    employee_id: int,
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if not employee:
        raise ValueError("Employee not found")

    risk = (
        db.query(EmployeeRisk)
        .filter(
            EmployeeRisk.employee_id == employee_id
        )
        .first()
    )

    if not risk:
        raise ValueError(
            "Risk information not available"
        )

    if risk.risk_level == "LOW":
        return {
            "message": "No alert required for low-risk employee",
            "alerts_created": 0,
        }

    if risk.risk_level == "HIGH":
        title = "High Attrition Risk Alert"

        message = (
            f"Employee {employee.first_name} "
            f"{employee.last_name} has been identified "
            f"as HIGH attrition risk. "
            f"Risk score: {risk.risk_score:.2f}. "
            f"Immediate HR attention is recommended."
        )

        notification_type = "ATTRITION_HIGH"
        priority = "HIGH"

    else:
        title = "Medium Attrition Risk Alert"

        message = (
            f"Employee {employee.first_name} "
            f"{employee.last_name} has been identified "
            f"as MEDIUM attrition risk. "
            f"Risk score: {risk.risk_score:.2f}. "
            f"Employee engagement should be monitored."
        )

        notification_type = "ATTRITION_MEDIUM"
        priority = "MEDIUM"

    recipients = (
        db.query(User)
        .filter(
            User.role.in_(
                ["ADMIN", "HR"]
            ),
            User.is_active.is_(True),
        )
        .all()
    )

    alerts_created = 0

    for user in recipients:

        existing = (
            db.query(Notification)
            .filter(
                Notification.user_id == user.id,
                Notification.notification_type
                == notification_type,
                Notification.is_read.is_(False),
            )
            .first()
        )

        if existing:
            continue

        notification = Notification(
            user_id=user.id,
            title=title,
            message=message,
            notification_type=notification_type,
            is_read=False,
        )

        db.add(notification)
        alerts_created += 1

    db.commit()

    return {
        "message": (
            f"{priority} attrition alert generated"
        ),
        "alerts_created": alerts_created,
    }