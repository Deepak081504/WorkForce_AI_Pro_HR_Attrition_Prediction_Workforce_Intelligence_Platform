from fastapi import APIRouter, Depends
from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_roles
from app.models.attrition_prediction import AttritionPrediction
from app.models.department import Department
from app.models.employee import Employee
from app.models.employee_risk import EmployeeRisk
from app.models.user import User
from app.schemas.attrition_analytics import (
    AttritionAnalyticsResponse,
    AttritionOverview,
    DepartmentRiskAnalytics,
    RiskDistribution,
)


router = APIRouter(
    prefix="/attrition-analytics",
    tags=["Attrition Analytics Dashboard"],
)


@router.get(
    "/dashboard",
    response_model=AttritionAnalyticsResponse,
)
def attrition_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("ADMIN", "HR")
    ),
):
    total_predictions = (
        db.query(AttritionPrediction)
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

    average_probability = (
        db.query(
            func.coalesce(
                func.avg(
                    AttritionPrediction
                    .attrition_probability
                ),
                0,
            )
        )
        .scalar()
    )

    risk_distribution = [
        RiskDistribution(
            risk_level="HIGH",
            employee_count=high_risk,
        ),
        RiskDistribution(
            risk_level="MEDIUM",
            employee_count=medium_risk,
        ),
        RiskDistribution(
            risk_level="LOW",
            employee_count=low_risk,
        ),
    ]

    department_results = (
        db.query(
            Department.id,
            Department.name,
            func.count(Employee.id),
            func.sum(
                case(
                    (
                        EmployeeRisk.risk_level
                        == "HIGH",
                        1,
                    ),
                    else_=0,
                )
            ),
            func.coalesce(
                func.avg(
                    EmployeeRisk.risk_score
                ),
                0,
            ),
        )
        .outerjoin(
            Employee,
            Employee.department_id
            == Department.id,
        )
        .outerjoin(
            EmployeeRisk,
            EmployeeRisk.employee_id
            == Employee.id,
        )
        .group_by(
            Department.id,
            Department.name,
        )
        .order_by(
            Department.id
        )
        .all()
    )

    department_analysis = [
        DepartmentRiskAnalytics(
            department_id=row[0],
            department_name=row[1],
            employee_count=row[2],
            high_risk_count=int(
                row[3] or 0
            ),
            average_risk_score=round(
                float(row[4] or 0),
                4,
            ),
        )
        for row in department_results
    ]

    return AttritionAnalyticsResponse(
        overview=AttritionOverview(
            total_predictions=total_predictions,
            high_risk=high_risk,
            medium_risk=medium_risk,
            low_risk=low_risk,
            average_attrition_probability=round(
                float(
                    average_probability or 0
                ),
                4,
            ),
        ),
        risk_distribution=risk_distribution,
        department_analysis=department_analysis,
    )