"""
Workforce headcount forecasting module.
"""

from datetime import datetime

import numpy as np
from sklearn.linear_model import LinearRegression


def forecast_workforce(
    historical_data: list[dict],
    periods_to_forecast: int = 3,
) -> list[dict]:
    """
    Forecast future workforce headcount
    using Linear Regression.
    """
    if len(historical_data) < 2:
        raise ValueError(
            "At least 2 historical data points "
            "are required."
        )

    if periods_to_forecast < 1:
        raise ValueError(
            "periods_to_forecast must be at least 1."
        )

    X = np.array(
        [
            [index]
            for index in range(
                len(historical_data)
            )
        ]
    )

    y = np.array(
        [
            item["headcount"]
            for item in historical_data
        ]
    )

    model = LinearRegression()

    model.fit(
        X,
        y,
    )

    last_period = historical_data[-1]["period"]

    try:
        year, month = map(
            int,
            last_period.split("-"),
        )
    except (ValueError, AttributeError):
        current = datetime.now()
        year = current.year
        month = current.month

    forecasts = []

    for i in range(
        1,
        periods_to_forecast + 1,
    ):
        future_index = (
            len(historical_data) + i - 1
        )

        predicted = model.predict(
            [[future_index]]
        )[0]

        predicted_headcount = max(
            0,
            round(float(predicted), 2),
        )

        future_month = month + i

        future_year = (
            year
            + (future_month - 1) // 12
        )

        future_month = (
            (future_month - 1) % 12
        ) + 1

        forecast_period = (
            f"{future_year:04d}-"
            f"{future_month:02d}"
        )

        forecasts.append(
            {
                "forecast_period": forecast_period,
                "predicted_headcount": predicted_headcount,
                "model_version": (
                    "linear_regression_v1"
                ),
            }
        )

    return forecasts


def calculate_growth_rate(
    historical_data: list[dict],
) -> float:
    """
    Calculate workforce growth percentage
    from first to last historical value.
    """
    if len(historical_data) < 2:
        return 0.0

    first = float(
        historical_data[0]["headcount"]
    )

    last = float(
        historical_data[-1]["headcount"]
    )

    if first == 0:
        return 0.0

    growth = (
        (last - first) / first
    ) * 100

    return round(
        growth,
        2,
    )