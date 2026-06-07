from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import User, ForecastHistory

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


def admin_required(current_user: User):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return current_user


@router.get("/users")
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    admin_required(current_user)

    users = db.query(User).all()

    return {
        "total_users": len(users),
        "users": [
            {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "role": user.role,
            }
            for user in users
        ]
    }


@router.get("/forecasts")
def get_forecasts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    admin_required(current_user)

    forecasts = db.query(ForecastHistory).all()

    return {
        "total_forecasts": len(forecasts),
        "forecasts": [
            {
                "id": item.id,
                "user_id": item.user_id,
                "energy_kwh": item.predicted_energy_kwh,
                "cost_usd": item.estimated_cost_usd,
                "carbon_kg": item.carbon_emission_kg,
                "peak_risk": item.peak_risk,
                "created_at": item.created_at,
            }
            for item in forecasts
        ]
    }


@router.get("/stats")
def admin_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    admin_required(current_user)

    users = db.query(User).count()
    forecasts = db.query(ForecastHistory).count()

    return {
        "platform_users": users,
        "total_forecasts": forecasts,
        "platform_status": "healthy",
        "version": "3.0.0"
    }