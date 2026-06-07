from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

from app.routes.admin import router as admin_router
from app.routes.analytics import router as analytics_router
from app.routes.auth import router as auth_router
from app.routes.export import router as export_router
from app.routes.forecast import router as forecast_router

# ============================================================
# DATABASE INITIALIZATION
# ============================================================

Base.metadata.create_all(bind=engine)

# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

app = FastAPI(
    title="Smart Energy Forecasting & Optimization Platform",
    description="""
    Industrial-style AI-powered energy analytics SaaS platform.

    Core Capabilities:
    - User Registration and JWT Authentication
    - Role-Based Admin Management
    - Energy Consumption Forecasting
    - Cost Estimation
    - Carbon Emission Calculation
    - Peak Risk Analysis
    - AI Optimization Recommendations
    - Forecast History Tracking
    - User-Level Analytics Dashboard
    - Admin-Level Platform Monitoring
    - CSV Report Export
    """,
    version="3.2.0",
)

# ============================================================
# CORS CONFIGURATION
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# ROUTERS
# ============================================================

app.include_router(auth_router)
app.include_router(forecast_router)
app.include_router(analytics_router)
app.include_router(admin_router)
app.include_router(export_router)

# ============================================================
# SYSTEM ENDPOINTS
# ============================================================

@app.get("/", tags=["System"])
def root():
    return {
        "project": "Smart Energy Forecasting & Optimization Platform",
        "version": "3.2.0",
        "status": "running",
        "environment": "development",
        "modules": {
            "authentication": "enabled",
            "forecasting": "enabled",
            "analytics": "enabled",
            "admin": "enabled",
            "export": "enabled",
            "database": "connected",
        },
    }


@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "api": "online",
        "database": "connected",
        "version": "3.2.0",
    }


# ============================================================
# STARTUP EVENT
# ============================================================

@app.on_event("startup")
def startup_event():
    print("=" * 70)
    print("SMART ENERGY FORECASTING & OPTIMIZATION PLATFORM")
    print("Version: 3.2.0")
    print("Authentication: Enabled")
    print("Forecast API: Enabled")
    print("Analytics API: Enabled")
    print("Admin API: Enabled")
    print("Export API: Enabled")
    print("Database: Connected")
    print("=" * 70)