from datetime import datetime

import numpy as np
from sklearn.linear_model import LinearRegression
from sqlalchemy.orm import Session

from app.models.workforce_forecast import (
    WorkforceForecast,
)
from app.schemas.forecast import (
    WorkforceForecastRequest,
)


def generate_forecast(
    db: Session,
    data: WorkforceForecastRequest,
):
    if len(data.historical_data) < 2:
        raise ValueError(
            "At least 2 historical data points are required"
        )

    historical = data.historical_data

    X = np.array(
        [
            [index]
            for index in range(len(historical))
        ]
    )

    y = np.array(
        [
            item.headcount
            for item in historical
        ]
    )

    model = LinearRegression()

    model.fit(X, y)

    forecasts = []

    last_period = historical[-1].period

    try:
        if "-" in last_period:
            year, month = map(
                int,
                last_period.split("-"),
            )
        else:
            raise ValueError

    except ValueError:
        year = datetime.now().year
        month = datetime.now().month

    for i in range(
        1,
        data.periods_to_forecast + 1,
    ):
        future_index = len(historical) + i - 1

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

        forecast = WorkforceForecast(
            forecast_period=forecast_period,
            predicted_headcount=predicted_headcount,
            model_version="linear_regression_v1",
        )

        db.add(forecast)

        forecasts.append(
            {
                "forecast_period": forecast_period,
                "predicted_headcount": predicted_headcount,
                "model_version": "linear_regression_v1",
            }
        )

    db.commit()

    return forecasts