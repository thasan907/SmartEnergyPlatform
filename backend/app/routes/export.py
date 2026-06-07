import io

import pandas as pd
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import ForecastHistory, User

router = APIRouter(prefix="/export", tags=["Export Reports"])


@router.get("/csv")
def export_forecast_csv(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    records = (
        db.query(ForecastHistory)
        .filter(ForecastHistory.user_id == current_user.id)
        .order_by(ForecastHistory.created_at.desc())
        .all()
    )

    data = [
        {
            "Date": record.created_at,
            "Predicted Energy (kWh)": record.predicted_energy_kwh,
            "Estimated Cost (USD)": record.estimated_cost_usd,
            "Carbon Emission (kg)": record.carbon_emission_kg,
            "Peak Risk": record.peak_risk,
            "Model": record.model_name,
        }
        for record in records
    ]

    df = pd.DataFrame(data)

    stream = io.StringIO()
    df.to_csv(stream, index=False)
    stream.seek(0)

    filename = f"smart_energy_report_user_{current_user.id}.csv"

    return StreamingResponse(
        iter([stream.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/pdf")
def export_forecast_pdf(
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

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    width, height = letter
    y = height - 50

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y, "Smart Energy Forecasting Report")

    y -= 30
    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"User: {current_user.full_name}")
    y -= 18
    pdf.drawString(50, y, f"Email: {current_user.email}")
    y -= 18
    pdf.drawString(50, y, "Platform: Smart Energy Forecasting & Optimization Platform")

    y -= 35
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y, "Recent Forecast Summary")

    y -= 25
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(50, y, "ID")
    pdf.drawString(85, y, "Energy")
    pdf.drawString(155, y, "Cost")
    pdf.drawString(220, y, "Carbon")
    pdf.drawString(300, y, "Risk")
    pdf.drawString(380, y, "Date")

    pdf.setFont("Helvetica", 9)

    for record in records:
        y -= 20

        if y < 70:
            pdf.showPage()
            y = height - 50
            pdf.setFont("Helvetica", 9)

        pdf.drawString(50, y, str(record.id))
        pdf.drawString(85, y, f"{record.predicted_energy_kwh} kWh")
        pdf.drawString(155, y, f"${record.estimated_cost_usd}")
        pdf.drawString(220, y, f"{record.carbon_emission_kg} kg")
        pdf.drawString(300, y, record.peak_risk)
        pdf.drawString(380, y, str(record.created_at)[:19])

    y -= 40
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "AI Optimization Recommendations")

    recommendations = [
        "Reduce evening peak-hour appliance usage.",
        "Shift laundry, dishwasher, and EV charging to off-peak periods.",
        "Monitor abnormal usage spikes through forecast history.",
        "Use weather-aware planning during high-temperature days.",
    ]

    pdf.setFont("Helvetica", 10)

    for item in recommendations:
        y -= 18
        pdf.drawString(65, y, f"- {item}")

    pdf.save()
    buffer.seek(0)

    filename = f"smart_energy_report_user_{current_user.id}.pdf"

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )