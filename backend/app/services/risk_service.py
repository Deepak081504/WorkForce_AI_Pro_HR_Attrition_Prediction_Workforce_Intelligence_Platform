from sqlalchemy.orm import Session

from app.models.attrition_prediction import (
    AttritionPrediction,
)
from app.models.employee_risk import EmployeeRisk


def get_risk_level(
    score: float,
) -> str:

    if score >= 0.70:
        return "HIGH"

    if score >= 0.40:
        return "MEDIUM"

    return "LOW"


def generate_risk_reason(
    prediction: AttritionPrediction,
) -> str:

    if prediction.risk_level == "HIGH":
        return (
            "Employee has a high predicted attrition "
            "probability and requires HR attention."
        )

    if prediction.risk_level == "MEDIUM":
        return (
            "Employee has a moderate attrition risk "
            "and should be monitored."
        )

    return (
        "Employee currently has a low predicted "
        "attrition risk."
    )


def update_employee_risk(
    db: Session,
    prediction: AttritionPrediction,
) -> EmployeeRisk:

    risk = (
        db.query(EmployeeRisk)
        .filter(
            EmployeeRisk.employee_id
            == prediction.employee_id
        )
        .first()
    )

    if not risk:
        risk = EmployeeRisk(
            employee_id=prediction.employee_id,
            risk_score=prediction.attrition_probability,
            risk_level=prediction.risk_level,
            risk_reason=generate_risk_reason(
                prediction
            ),
            last_prediction_id=prediction.id,
        )

        db.add(risk)

    else:
        risk.risk_score = (
            prediction.attrition_probability
        )

        risk.risk_level = (
            prediction.risk_level
        )

        risk.risk_reason = (
            generate_risk_reason(prediction)
        )

        risk.last_prediction_id = (
            prediction.id
        )

    db.commit()
    db.refresh(risk)

    return risk