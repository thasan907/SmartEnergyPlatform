import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

DATA_PATH = Path("data/processed/feature_engineered_data.csv")
MODEL_PATH = Path("ml/models/random_forest_model.pkl")
REPORT_PATH = Path("ml/reports/random_forest_report.json")

print("=" * 70)
print("SMART ENERGY PLATFORM - RANDOM FOREST TRAINING")
print("=" * 70)

print("\nLoading feature-engineered dataset...")
df = pd.read_csv(DATA_PATH)

print(f"Dataset Shape: {df.shape}")

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

target = "energy_sum"

df = df.dropna(subset=features + [target])

df["day"] = pd.to_datetime(df["day"])

df = df.sort_values("day")

split_date = df["day"].quantile(0.8)

train_df = df[df["day"] <= split_date]
test_df = df[df["day"] > split_date]

X_train = train_df[features]
y_train = train_df[target]

X_test = test_df[features]
y_test = test_df[target]

print(f"\nTraining Rows: {X_train.shape[0]}")
print(f"Testing Rows: {X_test.shape[0]}")

print("\nTraining Random Forest model...")

model = RandomForestRegressor(
    n_estimators=100,
    max_depth=15,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1,
)

model.fit(X_train, y_train)

print("\nMaking predictions...")
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\nModel Evaluation:")
print(f"MAE:  {mae:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"R2:   {r2:.4f}")

MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

joblib.dump(model, MODEL_PATH)

report = {
    "model": "Random Forest Regressor",
    "target": target,
    "features": features,
    "training_rows": int(X_train.shape[0]),
    "testing_rows": int(X_test.shape[0]),
    "metrics": {
        "MAE": float(mae),
        "RMSE": float(rmse),
        "R2": float(r2),
    },
}

with open(REPORT_PATH, "w") as file:
    json.dump(report, file, indent=4)

print("\nModel saved:")
print(MODEL_PATH)

print("\nReport saved:")
print(REPORT_PATH)