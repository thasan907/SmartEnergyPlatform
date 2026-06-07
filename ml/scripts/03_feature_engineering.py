import pandas as pd
from pathlib import Path

INPUT_PATH = Path("data/processed/daily_cleaned.csv")
OUTPUT_PATH = Path("data/processed/feature_engineered_data.csv")
SAMPLE_PATH = Path("data/sample/sample_feature_engineered_data.csv")

print("=" * 70)
print("SMART ENERGY PLATFORM - FEATURE ENGINEERING")
print("=" * 70)

print("\nLoading cleaned dataset...")
df = pd.read_csv(INPUT_PATH)

print(f"Original Shape: {df.shape}")

df["day"] = pd.to_datetime(df["day"])

df = df.sort_values(["LCLid", "day"]).reset_index(drop=True)

print("\nCreating date-based features...")
df["year"] = df["day"].dt.year
df["month"] = df["day"].dt.month
df["day_of_month"] = df["day"].dt.day
df["day_of_week"] = df["day"].dt.dayofweek
df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)
df["quarter"] = df["day"].dt.quarter

print("Creating lag features...")
df["lag_1"] = df.groupby("LCLid")["energy_sum"].shift(1)
df["lag_7"] = df.groupby("LCLid")["energy_sum"].shift(7)
df["lag_30"] = df.groupby("LCLid")["energy_sum"].shift(30)

print("Creating rolling average features...")
df["rolling_7_mean"] = (
    df.groupby("LCLid")["energy_sum"]
    .shift(1)
    .rolling(window=7, min_periods=1)
    .mean()
)

df["rolling_30_mean"] = (
    df.groupby("LCLid")["energy_sum"]
    .shift(1)
    .rolling(window=30, min_periods=1)
    .mean()
)

print("Creating consumption behavior features...")
df["daily_range"] = df["energy_max"] - df["energy_min"]
df["usage_variability"] = df["energy_std"]
df["peak_to_average_ratio"] = df["energy_max"] / (df["energy_mean"] + 0.001)

print("Removing rows with missing lag values...")
df = df.dropna(subset=["lag_1", "lag_7", "lag_30"])

df = df.reset_index(drop=True)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
SAMPLE_PATH.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_PATH, index=False)

sample_df = df.sample(min(5000, len(df)), random_state=42)
sample_df.to_csv(SAMPLE_PATH, index=False)

print("\nFeature Engineering Completed")
print(f"Final Shape: {df.shape}")
print(f"Saved full dataset: {OUTPUT_PATH}")
print(f"Saved sample dataset: {SAMPLE_PATH}")

print("\nFinal Columns:")
for col in df.columns:
    print(col)