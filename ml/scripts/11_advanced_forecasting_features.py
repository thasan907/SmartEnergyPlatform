import pandas as pd
from pathlib import Path

CLEAN_PATH = Path("data/processed/daily_cleaned.csv")
WEATHER_PATH = Path("data/raw/weather_daily_darksky.csv")
HOLIDAY_PATH = Path("data/raw/uk_bank_holidays.csv")

OUTPUT_PATH = Path("data/processed/advanced_forecasting_dataset.csv")
SAMPLE_PATH = Path("data/sample/sample_advanced_forecasting_dataset.csv")

print("=" * 70)
print("ADVANCED FORECASTING FEATURE ENGINEERING")
print("=" * 70)

df = pd.read_csv(CLEAN_PATH)
df["day"] = pd.to_datetime(df["day"])
df = df.sort_values(["LCLid", "day"]).reset_index(drop=True)

# Calendar features
df["year"] = df["day"].dt.year
df["month"] = df["day"].dt.month
df["day_of_month"] = df["day"].dt.day
df["day_of_week"] = df["day"].dt.dayofweek
df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)
df["quarter"] = df["day"].dt.quarter

# True target: next day consumption
df["target_energy_next_day"] = df.groupby("LCLid")["energy_sum"].shift(-1)

# Historical lag features
for lag in [1, 2, 3, 7, 14, 30, 60]:
    df[f"lag_{lag}"] = df.groupby("LCLid")["energy_sum"].shift(lag)

# Rolling mean features
for window in [3, 7, 14, 30, 60]:
    df[f"rolling_{window}_mean"] = (
        df.groupby("LCLid")["energy_sum"]
        .shift(1)
        .rolling(window=window, min_periods=1)
        .mean()
    )

# Rolling std features
for window in [7, 30]:
    df[f"rolling_{window}_std"] = (
        df.groupby("LCLid")["energy_sum"]
        .shift(1)
        .rolling(window=window, min_periods=1)
        .std()
    )

# Trend/change features
df["energy_change_1"] = df["lag_1"] - df["lag_2"]
df["energy_change_7"] = df["lag_1"] - df["lag_7"]
df["rolling_mean_gap"] = df["rolling_7_mean"] - df["rolling_30_mean"]

# Weather
weather = pd.read_csv(WEATHER_PATH)
weather["day"] = pd.to_datetime(weather["time"])
weather["day"] = weather["day"].dt.date

weather_cols = [
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

weather = weather[weather_cols]

df["merge_day"] = df["day"].dt.date

df = df.merge(
    weather,
    left_on="merge_day",
    right_on="day",
    how="left",
    suffixes=("", "_weather"),
)

df = df.drop(columns=["merge_day", "day_weather"])

# Holidays
holidays = pd.read_csv(HOLIDAY_PATH)
holidays["holiday_day"] = pd.to_datetime(holidays["Bank holidays"]).dt.date
holidays["is_holiday"] = 1
holidays = holidays[["holiday_day", "is_holiday", "Type"]]

df["merge_day"] = df["day"].dt.date

df = df.merge(
    holidays,
    left_on="merge_day",
    right_on="holiday_day",
    how="left",
)

df["is_holiday"] = df["is_holiday"].fillna(0).astype(int)
df["Type"] = df["Type"].fillna("None")

df = pd.get_dummies(df, columns=["Type"], prefix="holiday_type")

df = df.drop(columns=["merge_day", "holiday_day"])

# Fill weather missing values
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

# Remove rows with missing forecasting features
df = df.dropna()

# Remove leakage columns
leakage_cols = [
    "energy_median",
    "energy_mean",
    "energy_max",
    "energy_count",
    "energy_std",
    "energy_min",
]

df = df.drop(columns=leakage_cols)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
SAMPLE_PATH.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_PATH, index=False)

sample_df = df.sample(min(5000, len(df)), random_state=42)
sample_df.to_csv(SAMPLE_PATH, index=False)

print("\nAdvanced forecasting dataset created.")
print(f"Shape: {df.shape}")
print(f"Saved full dataset: {OUTPUT_PATH}")
print(f"Saved sample dataset: {SAMPLE_PATH}")

print("\nColumns:")
for col in df.columns:
    print(col)