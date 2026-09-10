from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.employee_risk import EmployeeRisk
from app.models.ai_recommendation import AIRecommendation


def generate_recommendation(
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
            EmployeeRisk.employee_id
            == employee_id
        )
        .first()
    )

    if not risk:
        raise ValueError(
            "No attrition risk data found for employee"
        )

    if risk.risk_level == "HIGH":
        recommendation_type = "RETENTION"
        priority = "HIGH"

        recommendation = (
            "Immediate retention action is recommended. "
            "HR should conduct a one-to-one discussion, "
            "review workload and compensation, identify "
            "employee concerns, and create a retention plan."
        )

    elif risk.risk_level == "MEDIUM":
        recommendation_type = "ENGAGEMENT"
        priority = "MEDIUM"

        recommendation = (
            "Employee engagement should be improved. "
            "Manager should conduct a regular check-in, "
            "review workload, career growth opportunities, "
            "job satisfaction, and workplace concerns."
        )

    else:
        recommendation_type = "MONITORING"
        priority = "LOW"

        recommendation = (
            "Employee currently has low attrition risk. "
            "Continue normal performance monitoring, "
            "employee engagement, and career development."
        )

    result = AIRecommendation(
        employee_id=employee_id,
        recommendation_type=recommendation_type,
        risk_level=risk.risk_level,
        recommendation=recommendation,
        priority=priority,
        status="PENDING",
        generated_by="rule_based_ai_v1",
    )

    db.add(result)
    db.commit()
    db.refresh(result)

    return result