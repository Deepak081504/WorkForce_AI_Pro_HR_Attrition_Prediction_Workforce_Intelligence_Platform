"""
HR recommendation engine based on employee attrition risk.
"""


def generate_recommendation(
    risk_level: str,
) -> dict:
    """
    Generate HR intervention recommendation.
    """
    risk_level = (
        str(risk_level)
        .strip()
        .upper()
    )

    if risk_level == "HIGH":
        return {
            "recommendation_type": "RETENTION",
            "priority": "HIGH",
            "recommendation": (
                "Immediate retention action is "
                "recommended. HR should conduct "
                "a one-to-one discussion, review "
                "workload and compensation, "
                "identify employee concerns, "
                "and create a retention plan."
            ),
        }

    if risk_level == "MEDIUM":
        return {
            "recommendation_type": "ENGAGEMENT",
            "priority": "MEDIUM",
            "recommendation": (
                "Employee engagement should be "
                "improved. The manager should "
                "conduct regular check-ins, "
                "review workload, career growth "
                "opportunities and workplace "
                "concerns."
            ),
        }

    return {
        "recommendation_type": "MONITORING",
        "priority": "LOW",
        "recommendation": (
            "Employee currently has low attrition "
            "risk. Continue normal performance "
            "monitoring, employee engagement "
            "and career development."
        ),
    }


def generate_employee_recommendation(
    employee_id: int,
    risk_level: str,
) -> dict:
    """
    Generate recommendation with employee ID.
    """
    recommendation = generate_recommendation(
        risk_level
    )

    return {
        "employee_id": employee_id,
        "risk_level": (
            str(risk_level).upper()
        ),
        **recommendation,
        "generated_by": "rule_based_ai_v1",
    }