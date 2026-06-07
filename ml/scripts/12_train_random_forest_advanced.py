import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

DATA_PATH = Path("data/processed/advanced_forecasting_dataset.csv")
MODEL_PATH = Path("ml/models/random_forest_advanced_model.pkl")
REPORT_PATH = Path("ml/reports/random_forest_advanced_report.json")

print("=" * 70)
print("ADVANCED RANDOM FOREST FORECAST MODEL")
print("=" * 70)

df = pd.read_csv(DATA_PATH)
df["day"] = pd.to_datetime(df["day"])
df = df.sort_values("day")

target = "target_energy_next_day"

features = [
    col for col in df.columns
    if col not in ["LCLid", "day", target]
]

split_date = df["day"].quantile(0.8)

train_df = df[df["day"] <= split_date]
test_df = df[df["day"] > split_date]

X_train = train_df[features]
y_train = train_df[target]

X_test = test_df[features]
y_test = test_df[target]

print(f"Training rows: {len(X_train)}")
print(f"Testing rows: {len(X_test)}")
print(f"Total features: {len(features)}")

model = RandomForestRegressor(
    n_estimators=80,
    max_depth=18,
    min_samples_split=8,
    min_samples_leaf=4,
    random_state=42,
    n_jobs=-1
)

print("\nTraining advanced Random Forest...")
model.fit(X_train, y_train)

print("Making predictions...")
predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
r2 = r2_score(y_test, predictions)

print("\nResults")
print(f"MAE  : {mae:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"R²   : {r2:.4f}")

MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

joblib.dump(model, MODEL_PATH)

report = {
    "model": "Advanced Random Forest Forecast",
    "features": features,
    "MAE": float(mae),
    "RMSE": float(rmse),
    "R2": float(r2)
}

with open(REPORT_PATH, "w") as f:
    json.dump(report, f, indent=4)

print("\nSaved Model:")
print(MODEL_PATH)

print("\nSaved Report:")
print(REPORT_PATH)
