# Smart Energy Forecasting & Optimization Platform

An AI-powered Smart Energy Forecasting Platform built using FastAPI, React, Machine Learning, SQLite, and Data Analytics.

The platform predicts energy consumption, estimates operational costs, calculates carbon emissions, classifies energy usage risk, stores historical forecasts, and generates downloadable reports.

---

## Features

### Authentication & Security
- JWT Authentication
- Protected API Routes
- User Login System

### AI Forecasting
- Machine Learning Energy Prediction
- Random Forest Forecasting Model
- Dynamic Forecast Generation

### Analytics
- Energy Consumption Analysis
- Daily Cost Estimation
- Monthly Cost Projection
- Carbon Emission Calculation
- Risk Classification

### Data Management
- SQLite Database Integration
- Historical Forecast Storage
- Forecast Tracking Dashboard

### Reporting
- CSV Export
- PDF Report Generation
- Forecast History Export

### Visualization
- Interactive Dashboard
- Energy Trend Charts
- Cost Analytics
- KPI Monitoring Cards

---

## Technology Stack

### Frontend
- React
- Vite
- Axios
- Recharts
- CSS3

### Backend
- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication

### Machine Learning
- Scikit-Learn
- Random Forest Regressor
- NumPy
- Pandas

---

## Project Architecture

```text
Frontend (React)
       |
       v
FastAPI Backend
       |
       v
Machine Learning Model
       |
       v
SQLite Database
```

---

## Screenshots

### Login Page

![Login Page](screenshots/01-login-page.png)

### Dashboard

![Dashboard](screenshots/02-dashboard-hero.png)

### Analytics Dashboard

![Analytics Dashboard](screenshots/03-analytics-dashboard.png)

### Forecast History

![Forecast History](screenshots/04-forecast-history.png)

### CSV Export

![CSV Export](screenshots/05-export-csv.png)

### PDF Report

![PDF Report](screenshots/06-export-pdf.png)

---

## Installation

### Clone Repository

```bash
git clone YOUR_REPOSITORY_URL
```

### Backend Setup

```bash
cd backend

pip install -r requirements.txt

uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

### Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

---

## API Endpoints

### Authentication

```http
POST /auth/login
```

### Forecast

```http
POST /predict
```

### Forecast History

```http
GET /forecast/history
```

### Export CSV

```http
GET /export/csv
```

### Export PDF

```http
GET /export/pdf
```

---

## Sample Forecast Output

```json
{
  "predicted_energy_kwh": 8.45,
  "estimated_cost_usd": 1.27,
  "monthly_cost_usd": 38.10,
  "carbon_emission_kg": 1.96,
  "peak_risk": "Medium"
}
```

---

## Future Improvements

- Real Smart Meter Integration
- IoT Sensor Connectivity
- Weather-Based Forecasting
- Deep Learning Forecast Models
- Cloud Deployment
- Multi-User Support
- Real-Time Monitoring Dashboard

---

## Author

**Toufique Hasan**

M.S. Applied Computer Science  
Southeast Missouri State University

GitHub:
https://github.com/thasan907

LinkedIn:
https://linkedin.com

---

## License

This project is intended for educational, research, and portfolio purposes.