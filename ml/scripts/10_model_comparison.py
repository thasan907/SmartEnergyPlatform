import json
import pandas as pd

with open("ml/reports/random_forest_forecast_report.json") as f:
    rf = json.load(f)

with open("ml/reports/xgboost_forecast_report.json") as f:
    xgb = json.load(f)

results = pd.DataFrame([
    {
        "Model": "Random Forest",
        "MAE": rf["metrics"]["MAE"],
        "RMSE": rf["metrics"]["RMSE"],
        "R2": rf["metrics"]["R2"]
    },
    {
        "Model": "XGBoost",
        "MAE": xgb["MAE"],
        "RMSE": xgb["RMSE"],
        "R2": xgb["R2"]
    }
])

results = results.sort_values(
    by="R2",
    ascending=False
)

print("\nMODEL COMPARISON")
print("=" * 60)
print(results)

results.to_csv(
    "ml/reports/model_comparison.csv",
    index=False
)

print("\nSaved:")
print("ml/reports/model_comparison.csv")