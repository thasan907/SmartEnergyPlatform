import pandas as pd
from pathlib import Path

FORECAST_PATH = Path("data/processed/forecasting_dataset.csv")
WEATHER_PATH = Path("data/raw/weather_daily_darksky.csv")
HOLIDAY_PATH = Path("data/raw/uk_bank_holidays.csv")

OUTPUT_PATH = Path("data/processed/forecasting_dataset_v2.csv")
SAMPLE_PATH = Path("data/sample/sample_forecasting_dataset_v2.csv")

print("=" * 70)
print("WEATHER + HOLIDAY FEATURE INTEGRATION")
print("=" * 70)

print("\nLoading forecasting dataset...")
df = pd.read_csv(FORECAST_PATH)
df["day"] = pd.to_datetime(df["day"]).dt.date

print("Loading weather dataset...")
weather = pd.read_csv(WEATHER_PATH)

weather["day"] = pd.to_datetime(weather["time"]).dt.date

weather_features = [
    "day",
    "temperatureMax",
    "temperatureMin",
    "temperatureHigh",
    "temperatureLow",
    "humidity",
    "windSpeed",
    "pressure",
    "cloudCover",
    "visibility",
    "uvIndex",
    "dewPoint",
]

weather = weather[weather_features]

print("Loading holiday dataset...")
holidays = pd.read_csv(HOLIDAY_PATH)

holidays["day"] = pd.to_datetime(holidays["Bank holidays"]).dt.date
holidays["is_holiday"] = 1
holidays["holiday_type"] = holidays["Type"]

holidays = holidays[
    [
        "day",
        "is_holiday",
        "holiday_type",
    ]
]

print("\nMerging weather data...")
df = df.merge(weather, on="day", how="left")

print("Merging holiday data...")
df = df.merge(holidays, on="day", how="left")

df["is_holiday"] = df["is_holiday"].fillna(0).astype(int)
df["holiday_type"] = df["holiday_type"].fillna("None")

print("\nHandling missing weather values...")
weather_numeric_cols = [
    "temperatureMax",
    "temperatureMin",
    "temperatureHigh",
    "temperatureLow",
    "humidity",
    "windSpeed",
    "pressure",
    "cloudCover",
    "visibility",
    "uvIndex",
    "dewPoint",
]

for col in weather_numeric_cols:
    df[col] = df[col].fillna(df[col].median())

print("Encoding holiday type...")
df = pd.get_dummies(df, columns=["holiday_type"], drop_first=True)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
SAMPLE_PATH.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_PATH, index=False)

sample_df = df.sample(min(5000, len(df)), random_state=42)
sample_df.to_csv(SAMPLE_PATH, index=False)

print("\nIntegration completed successfully.")
print(f"Final shape: {df.shape}")
print(f"Saved full dataset: {OUTPUT_PATH}")
print(f"Saved sample dataset: {SAMPLE_PATH}")

print("\nFinal columns:")
for col in df.columns:
    print(col)
