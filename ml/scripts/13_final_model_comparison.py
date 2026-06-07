import json
from pathlib import Path

import pandas as pd

REPORTS = [
    {
        "name": "Random Forest Basic Forecast",
        "path": Path("ml/reports/random_forest_forecast_report.json"),
        "format": "metrics",
    },
    {
        "name": "XGBoost Forecast",
        "path": Path("ml/reports/xgboost_forecast_report.json"),
        "format": "flat",
    },
    {
        "name": "Advanced Random Forest",
        "path": Path("ml/reports/random_forest_advanced_report.json"),
        "format": "flat",
    },
]

rows = []

for report in REPORTS:
    with open(report["path"], "r") as file:
        data = json.load(file)

    if report["format"] == "metrics":
        mae = data["metrics"]["MAE"]
        rmse = data["metrics"]["RMSE"]
        r2 = data["metrics"]["R2"]
    else:
        mae = data["MAE"]
        rmse = data["RMSE"]
        r2 = data["R2"]

    rows.append(
        {
            "Model": report["name"],
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2,
        }
    )

comparison = pd.DataFrame(rows)

comparison = comparison.sort_values(
    by="R2",
    ascending=False
).reset_index(drop=True)

comparison["Rank"] = comparison.index + 1

comparison = comparison[
    [
        "Rank",
        "Model",
        "MAE",
        "RMSE",
        "R2",
    ]
]

output_path = Path("ml/reports/final_model_comparison.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

comparison.to_csv(output_path, index=False)

print("=" * 70)
print("FINAL MODEL COMPARISON")
print("=" * 70)
print(comparison)

print("\nBest Model:")
print(comparison.iloc[0]["Model"])

print("\nSaved:")
print(output_path)