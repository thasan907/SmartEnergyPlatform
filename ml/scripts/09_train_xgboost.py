import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

DATA_PATH = Path("data/processed/forecasting_dataset_v2.csv")

MODEL_PATH = Path("ml/models/xgboost_forecast_model.pkl")

REPORT_PATH = Path("ml/reports/xgboost_forecast_report.json")

print("=" * 70)
print("XGBOOST FORECAST MODEL")
print("=" * 70)

df = pd.read_csv(DATA_PATH)

df["day"] = pd.to_datetime(df["day"])

feature_cols = [
    col
    for col in df.columns
    if col not in ["LCLid", "day", "target_energy_next_day"]
]

target = "target_energy_next_day"

split_date = df["day"].quantile(0.8)

train_df = df[df["day"] <= split_date]
test_df = df[df["day"] > split_date]

X_train = train_df[feature_cols]
y_train = train_df[target]

X_test = test_df[feature_cols]
y_test = test_df[target]

print(f"Training Rows: {len(X_train)}")
print(f"Testing Rows: {len(X_test)}")

model = XGBRegressor(
    n_estimators=300,
    max_depth=8,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1
)

print("\nTraining XGBoost...")

model.fit(X_train, y_train)

print("\nMaking Predictions...")

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)

rmse = np.sqrt(
    mean_squared_error(y_test, predictions)
)

r2 = r2_score(y_test, predictions)

print("\nResults")
print(f"MAE  : {mae:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"R²   : {r2:.4f}")

MODEL_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

REPORT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

joblib.dump(
    model,
    MODEL_PATH
)

report = {
    "model": "XGBoost",
    "MAE": float(mae),
    "RMSE": float(rmse),
    "R2": float(r2)
}

with open(REPORT_PATH, "w") as f:
    json.dump(
        report,
        f,
        indent=4
    )

print("\nSaved Model:")
print(MODEL_PATH)

print("\nSaved Report:")
print(REPORT_PATH)