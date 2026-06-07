from pathlib import Path
import json
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[3]

MODEL_PATH = BASE_DIR / "ml" / "models" / "random_forest_advanced_model.pkl"
REPORT_PATH = BASE_DIR / "ml" / "reports" / "random_forest_advanced_report.json"

model = joblib.load(MODEL_PATH)

with open(REPORT_PATH, "r") as file:
    report = json.load(file)

FEATURES = report["features"]

def predict_energy(input_data: dict):
    row = {}

    for feature in FEATURES:
        row[feature] = input_data.get(feature, 0)

    df = pd.DataFrame([row])
    df = df[FEATURES]

    prediction = model.predict(df)[0]

    return round(float(prediction), 2)