from sqlalchemy.orm import Session

from app.models.employee_risk import EmployeeRisk
from app.models.hr_intervention import HRIntervention


def generate_recommendation(
    risk: EmployeeRisk,
):
    if risk.risk_level == "HIGH":
        return {
            "intervention_type": "RETENTION",
            "recommendation": (
                "Schedule a one-to-one HR discussion, "
                "review workload and compensation, "
                "and create a personalized retention plan."
            ),
            "priority": "HIGH",
        }

    if risk.risk_level == "MEDIUM":
        return {
            "intervention_type": "ENGAGEMENT",
            "recommendation": (
                "Schedule a manager check-in, review "
                "employee satisfaction, and identify "
                "possible workload or career-growth concerns."
            ),
            "priority": "MEDIUM",
        }

    return {
        "intervention_type": "MONITORING",
        "recommendation": (
            "Continue regular employee engagement "
            "and monitor future attrition risk changes."
        ),
        "priority": "LOW",
    }


def create_intervention(
    db: Session,
    employee_id: int,
    created_by: int,
):
    risk = (
        db.query(EmployeeRisk)
        .filter(
            EmployeeRisk.employee_id == employee_id
        )
        .first()
    )

    if not risk:
        raise ValueError(
            "Risk information not available for this employee"
        )

    recommendation = generate_recommendation(
        risk
    )

    intervention = HRIntervention(
        employee_id=employee_id,
        risk_level=risk.risk_level,
        intervention_type=(
            recommendation["intervention_type"]
        ),
        recommendation=(
            recommendation["recommendation"]
        ),
        priority=recommendation["priority"],
        status="PENDING",
        created_by=created_by,
    )

    db.add(intervention)
    db.commit()
    db.refresh(intervention)

    return intervention