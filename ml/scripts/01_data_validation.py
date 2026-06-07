import pandas as pd
from pathlib import Path

print("=" * 70)
print("SMART ENERGY FORECASTING & OPTIMIZATION PLATFORM")
print("PHASE 1 - DATA VALIDATION")
print("=" * 70)

DATA_PATH = Path("data/raw/daily_dataset.csv")

print("\nLoading dataset...")

df = pd.read_csv(DATA_PATH)

print("\nDataset Loaded Successfully")

print("\n" + "=" * 70)
print("DATASET SHAPE")
print("=" * 70)

print(df.shape)

print("\n" + "=" * 70)
print("COLUMN NAMES")
print("=" * 70)

for col in df.columns:
    print(col)

print("\n" + "=" * 70)
print("FIRST 5 ROWS")
print("=" * 70)

print(df.head())

print("\n" + "=" * 70)
print("DATA TYPES")
print("=" * 70)

print(df.dtypes)

print("\n" + "=" * 70)
print("MISSING VALUES")
print("=" * 70)

print(df.isnull().sum())

print("\n" + "=" * 70)
print("DUPLICATE ROWS")
print("=" * 70)

print(df.duplicated().sum())

print("\n" + "=" * 70)
print("MEMORY USAGE")
print("=" * 70)

memory_mb = df.memory_usage(deep=True).sum() / 1024**2

print(f"{memory_mb:.2f} MB")