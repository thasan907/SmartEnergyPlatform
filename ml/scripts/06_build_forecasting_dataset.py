import pandas as pd
from pathlib import Path

INPUT_PATH = Path("data/processed/feature_engineered_data.csv")
OUTPUT_PATH = Path("data/processed/forecasting_dataset.csv")
SAMPLE_PATH = Path("data/sample/sample_forecasting_dataset.csv")

print("=" * 70)
print("BUILDING TRUE FORECASTING DATASET")
print("=" * 70)

df = pd.read_csv(INPUT_PATH)
df["day"] = pd.to_datetime(df["day"])
df = df.sort_values(["LCLid", "day"]).reset_index(drop=True)

df["target_energy_next_day"] = df.groupby("LCLid")["energy_sum"].shift(-1)

forecast_df = df[
    [
        "LCLid",
        "day",
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
        "target_energy_next_day",
    ]
].dropna()

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
SAMPLE_PATH.parent.mkdir(parents=True, exist_ok=True)

forecast_df.to_csv(OUTPUT_PATH, index=False)

sample_df = forecast_df.sample(min(5000, len(forecast_df)), random_state=42)
sample_df.to_csv(SAMPLE_PATH, index=False)

print("\nForecasting dataset created successfully.")
print(f"Shape: {forecast_df.shape}")
print(f"Saved full dataset: {OUTPUT_PATH}")
print(f"Saved sample dataset: {SAMPLE_PATH}")