import os

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


def generate_training_data(n_samples: int = 5000) -> pd.DataFrame:
    np.random.seed(42)

    hours = np.random.randint(0, 24, n_samples)
    is_weekday = np.random.randint(0, 2, n_samples)
    is_raining = np.random.randint(0, 2, n_samples)
    has_match = np.random.randint(0, 2, n_samples)
    hours_to_match = np.where(has_match, np.random.randint(0, 4, n_samples), 0)

    base = 500

    hour_effect = np.where(
        (hours >= 7) & (hours <= 9),
        1500,
        np.where(
            (hours >= 17) & (hours <= 19),
            1800,
            np.where((hours >= 12) & (hours <= 14), 800, 200),
        ),
    )

    weekday_effect = is_weekday * 600
    rain_effect = is_raining * 400
    match_effect = np.where(hours_to_match <= 2, has_match * 1200, has_match * 300)
    noise = np.random.normal(0, 100, n_samples)

    passengers = (
        base + hour_effect + weekday_effect + rain_effect + match_effect + noise
    )
    passengers = np.clip(passengers, 0, 5000)

    return pd.DataFrame(
        {
            "hour": hours,
            "is_weekday": is_weekday,
            "is_raining": is_raining,
            "has_match": has_match,
            "hours_to_match": hours_to_match,
            "passengers": passengers.astype(int),
        }
    )


def train_model():
    df = generate_training_data()

    X = df.drop("passengers", axis=1)
    y = df["passengers"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)
    print(f"Model R² skoru: {score:.3f}")

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/passenger_model.pkl")
    return model


def load_or_train_model():
    model_path = "models/passenger_model.pkl"
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return train_model()
