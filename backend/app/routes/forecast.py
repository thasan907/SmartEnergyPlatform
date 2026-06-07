from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import ForecastHistory, User
from app.services.predictor import predict_energy

router = APIRouter(tags=["Forecast"])

MODEL_NAME = "Advanced Random Forest"
MODEL_ACCURACY = 85.93
ENERGY_RATE_USD = 0.15
CARBON_FACTOR_KG_PER_KWH = 0.233


class ForecastInput(BaseModel):
    year: int = 2014
    month: int = 6
    day_of_month: int = 15
    day_of_week: int = 2
    is_weekend: int = 0
    quarter: int = 2

    lag_1: float = 10.2
    lag_2: float = 10.0
    lag_3: float = 9.9
    lag_7: float = 9.8
    lag_14: float = 10.1
    lag_30: float = 11.3
    lag_60: float = 10.5

    rolling_3_mean: float = 10.1
    rolling_7_mean: float = 10.1
    rolling_14_mean: float = 10.4
    rolling_30_mean: float = 10.8
    rolling_60_mean: float = 10.6

    rolling_7_std: float = 1.2
    rolling_30_std: float = 1.5

    energy_change_1: float = 0.2
    energy_change_7: float = 0.4
    rolling_mean_gap: float = -0.7

    temperatureMax: float = 28
    temperatureMin: float = 18
    temperatureHigh: float = 29
    temperatureLow: float = 17
    humidity: float = 0.65
    windSpeed: float = 11
    pressure: float = 1015
    cloudCover: float = 0.4
    visibility: float = 10
    uvIndex: float = 5
    dewPoint: float = 9
    is_holiday: int = 0


def calculate_peak_risk(predicted_kwh: float):
    if predicted_kwh >= 12:
        return "High"
    if predicted_kwh >= 8:
        return "Medium"
    return "Low"


def calculate_savings_potential(risk: str):
    if risk == "High":
        return 18
    if risk == "Medium":
        return 12
    return 6


def build_recommendations(risk: str):
    if risk == "High":
        return [
            "High peak-risk detected. Shift major appliance usage to off-peak hours.",
            "Investigate abnormal consumption spikes and appliance inefficiency.",
            "Monitor daily consumption against the 30-day rolling average.",
            "Use weather-aware planning during high-temperature days.",
        ]

    if risk == "Medium":
        return [
            "Moderate peak-risk detected. Reduce evening usage between 6 PM and 9 PM.",
            "Shift laundry, dishwasher, and charging to lower-demand periods.",
            "Monitor daily consumption against the 30-day rolling average.",
            "Use weather-aware planning during high-temperature days.",
        ]

    return [
        "Energy usage is stable. Continue maintaining efficient consumption habits.",
        "Monitor daily consumption against the 30-day rolling average.",
        "Use weather-aware planning during high-temperature days.",
    ]


@router.get("/forecast")
def forecast_status():
    return {
        "message": "Use POST /predict for authenticated ML forecast",
        "best_model": MODEL_NAME,
        "model_accuracy_percent": MODEL_ACCURACY,
        "status": "ready",
    }


@router.post("/predict")
def predict(
    data: ForecastInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    predicted_kwh = predict_energy(data.model_dump())
    estimated_cost = round(predicted_kwh * ENERGY_RATE_USD, 2)
    carbon_emission = round(predicted_kwh * CARBON_FACTOR_KG_PER_KWH, 2)

    peak_risk = calculate_peak_risk(predicted_kwh)
    savings_potential = calculate_savings_potential(peak_risk)
    recommendations = build_recommendations(peak_risk)

    history = ForecastHistory(
        user_id=current_user.id,
        predicted_energy_kwh=predicted_kwh,
        estimated_cost_usd=estimated_cost,
        carbon_emission_kg=carbon_emission,
        peak_risk=peak_risk,
        model_name=MODEL_NAME,
    )

    db.add(history)
    db.commit()
    db.refresh(history)

    return {
        "id": history.id,
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "role": current_user.role,
        },
        "model": MODEL_NAME,
        "predicted_energy_kwh": predicted_kwh,
        "model_accuracy_percent": MODEL_ACCURACY,
        "estimated_cost_usd": estimated_cost,
        "carbon_emission_kg": carbon_emission,
        "peak_risk": peak_risk,
        "savings_potential_percent": savings_potential,
        "recommendations": recommendations,
        "unit": "kWh",
        "status": "success",
    }


@router.get("/forecast/week")
def weekly_forecast():
    return {
        "weekly_forecast": [
            {"day": "Mon", "usage": 8.9},
            {"day": "Tue", "usage": 9.4},
            {"day": "Wed", "usage": 8.7},
            {"day": "Thu", "usage": 9.1},
            {"day": "Fri", "usage": 9.8},
            {"day": "Sat", "usage": 10.2},
            {"day": "Sun", "usage": 9.5},
        ]
    }


@router.get("/forecast/history")
def forecast_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    records = (
        db.query(ForecastHistory)
        .filter(ForecastHistory.user_id == current_user.id)
        .order_by(ForecastHistory.created_at.desc())
        .limit(10)
        .all()
    )

    return {
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "role": current_user.role,
        },
        "count": len(records),
        "history": [
            {
                "id": record.id,
                "predicted_energy_kwh": record.predicted_energy_kwh,
                "estimated_cost_usd": record.estimated_cost_usd,
                "carbon_emission_kg": record.carbon_emission_kg,
                "peak_risk": record.peak_risk,
                "model_name": record.model_name,
                "created_at": record.created_at,
            }
            for record in records
        ],
    }