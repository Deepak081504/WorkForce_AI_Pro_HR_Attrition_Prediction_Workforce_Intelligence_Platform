"""
Employee attrition risk analysis engine.
"""


def calculate_risk_level(
    probability: float,
) -> str:
    """
    Convert probability into LOW, MEDIUM or HIGH.
    """
    probability = float(probability)

    if probability >= 0.70:
        return "HIGH"

    if probability >= 0.40:
        return "MEDIUM"

    return "LOW"


def generate_risk_reason(
    probability: float,
) -> str:
    """
    Generate a simple explanation for the risk level.
    """
    risk_level = calculate_risk_level(
        probability
    )

    if risk_level == "HIGH":
        return (
            "Employee has a high predicted "
            "attrition probability and requires "
            "immediate HR attention."
        )

    if risk_level == "MEDIUM":
        return (
            "Employee has a moderate attrition "
            "risk and should be monitored by HR."
        )

    return (
        "Employee currently has a low predicted "
        "attrition risk."
    )


def analyze_employee_risk(
    probability: float,
) -> dict:
    """
    Return complete employee risk information.
    """
    probability = round(
        float(probability),
        4,
    )

    risk_level = calculate_risk_level(
        probability
    )

    return {
        "risk_score": probability,
        "risk_level": risk_level,
        "risk_reason": generate_risk_reason(
            probability
        ),
    }