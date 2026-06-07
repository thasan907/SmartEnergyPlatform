import joblib
import pandas as pd
from pathlib import Path

MODEL_PATH = Path("ml/models/random_forest_model.pkl")

model = joblib.load(MODEL_PATH)

features = [
    "energy_median",
    "energy_mean",
    "energy_max",
    "energy_count",
    "energy_std",
    "energy_min",
    "year",
    "month",
    "day_of_month",
    "day_of_week",
    "is_weekend",
    "quarter",
    "lag_1",
    "lag_7",
    "lag_30",
    "rolling_7_mean",
    "rolling_30_mean",
    "daily_range",
    "usage_variability",
    "peak_to_average_ratio",
]

importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print(importance)