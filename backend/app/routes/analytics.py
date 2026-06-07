from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.auth import get_current_user
from app.database import get_db
from app.models import ForecastHistory, User

router = APIRouter(tags=["Analytics"])


@router.get("/analytics/summary")
def analytics_summary():
    return {
        "total_consumption_kwh": 245.8,
        "estimated_monthly_bill_usd": 36.87,
        "efficiency_score": 87,
        "savings_potential_percent": 12,
        "peak_usage_period": "Evening",
        "risk_level": "Medium",
        "carbon_emission_kg": 57.26,
        "status": "stable",
    }


@router.get("/analytics/dashboard")
def analytics_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    records = (
        db.query(ForecastHistory)
        .filter(ForecastHistory.user_id == current_user.id)
        .all()
    )

    if not records:
        return {
            "user": current_user.email,
            "total_forecasts": 0,
            "avg_energy_kwh": 0,
            "avg_cost_usd": 0,
            "avg_carbon_kg": 0,
            "highest_energy_kwh": 0,
            "lowest_energy_kwh": 0,
            "risk_distribution": {
                "Low": 0,
                "Medium": 0,
                "High": 0,
            },
        }

    total_forecasts = len(records)
    avg_energy = round(sum(r.predicted_energy_kwh for r in records) / total_forecasts, 2)
    avg_cost = round(sum(r.estimated_cost_usd for r in records) / total_forecasts, 2)
    avg_carbon = round(sum(r.carbon_emission_kg for r in records) / total_forecasts, 2)

    highest_energy = max(r.predicted_energy_kwh for r in records)
    lowest_energy = min(r.predicted_energy_kwh for r in records)

    risk_distribution = {
        "Low": 0,
        "Medium": 0,
        "High": 0,
    }

    for record in records:
        risk_distribution[record.peak_risk] += 1

    return {
        "user": current_user.email,
        "total_forecasts": total_forecasts,
        "avg_energy_kwh": avg_energy,
        "avg_cost_usd": avg_cost,
        "avg_carbon_kg": avg_carbon,
        "highest_energy_kwh": highest_energy,
        "lowest_energy_kwh": lowest_energy,
        "risk_distribution": risk_distribution,
    }


@router.get("/recommendations")
def recommendations():
    return {
        "recommendations": [
            "Reduce high-consumption appliance usage during peak evening hours.",
            "Shift laundry, dishwasher, and charging activity to off-peak times.",
            "Monitor abnormal usage spikes using daily anomaly alerts.",
            "Keep daily usage below the 30-day rolling average.",
            "Use weather-aware planning during high-temperature days.",
        ]
    }


@router.get("/models/comparison")
def model_comparison():
    return {
        "best_model": "Advanced Random Forest",
        "models": [
            {
                "name": "Advanced Random Forest",
                "mae": 2.1433,
                "rmse": 3.8098,
                "r2": 0.8593,
            },
            {
                "name": "Random Forest Basic",
                "mae": 2.2981,
                "rmse": 4.1632,
                "r2": 0.8286,
            },
            {
                "name": "XGBoost",
                "mae": 2.3177,
                "rmse": 4.2965,
                "r2": 0.8168,
            },
        ],
    }