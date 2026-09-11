"""
Workforce stability analysis engine.
"""


def calculate_stability_score(
    low_risk: int,
    medium_risk: int,
    high_risk: int,
) -> float:
    """
    Calculate workforce stability score.

    Low-risk employees contribute positively.
    Medium-risk employees have moderate impact.
    High-risk employees have the highest negative impact.
    """
    total = (
        low_risk
        + medium_risk
        + high_risk
    )

    if total == 0:
        return 0.0

    weighted_score = (
        (low_risk * 1.0)
        + (medium_risk * 0.5)
        + (high_risk * 0.0)
    )

    score = (
        weighted_score / total
    ) * 100

    return round(
        score,
        2,
    )


def get_stability_level(
    stability_score: float,
) -> str:
    """
    Convert stability score into a category.
    """
    score = float(stability_score)

    if score >= 75:
        return "STABLE"

    if score >= 50:
        return "MODERATE"

    return "AT_RISK"


def analyze_workforce_stability(
    low_risk: int,
    medium_risk: int,
    high_risk: int,
) -> dict:
    """
    Return complete workforce stability analysis.
    """
    score = calculate_stability_score(
        low_risk=low_risk,
        medium_risk=medium_risk,
        high_risk=high_risk,
    )

    level = get_stability_level(
        score
    )

    return {
        "stability_score": score,
        "stability_level": level,
        "low_risk_employees": low_risk,
        "medium_risk_employees": medium_risk,
        "high_risk_employees": high_risk,
    }