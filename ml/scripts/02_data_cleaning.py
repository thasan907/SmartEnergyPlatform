import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/daily_dataset.csv")
OUTPUT_PATH = Path("data/processed/daily_cleaned.csv")

print("Loading dataset...")

df = pd.read_csv(RAW_PATH)

print(f"Original Shape: {df.shape}")

# Convert date
df["day"] = pd.to_datetime(df["day"])

# Sort
df = df.sort_values(["LCLid", "day"])

# Fill missing energy_std
df["energy_std"] = df["energy_std"].fillna(0)

# Remove rows with missing target
df = df.dropna(subset=["energy_sum"])

# Remove negative values
df = df[df["energy_sum"] >= 0]

# Reset index
df = df.reset_index(drop=True)

# Save
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_PATH, index=False)

print(f"Cleaned Shape: {df.shape}")

print("Saved:")
print(OUTPUT_PATH)