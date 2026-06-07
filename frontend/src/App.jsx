import { useEffect, useState } from "react";
import axios from "axios";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import "./App.css";

const API = "http://127.0.0.1:8001";

const createForecastInput = () => {
  const today = new Date();

  const random = (min, max) =>
    Number((Math.random() * (max - min) + min).toFixed(2));

  const baseUsage = random(7.5, 15.5);

  return {
    year: today.getFullYear(),
    month: today.getMonth() + 1,
    day_of_month: today.getDate(),
    day_of_week: today.getDay(),
    is_weekend: [0, 6].includes(today.getDay()) ? 1 : 0,
    quarter: Math.ceil((today.getMonth() + 1) / 3),

    lag_1: random(baseUsage - 1.2, baseUsage + 1.2),
    lag_2: random(baseUsage - 1.4, baseUsage + 1.4),
    lag_3: random(baseUsage - 1.6, baseUsage + 1.6),
    lag_7: random(baseUsage - 2.0, baseUsage + 2.0),
    lag_14: random(baseUsage - 2.2, baseUsage + 2.2),
    lag_30: random(baseUsage - 2.5, baseUsage + 2.5),
    lag_60: random(baseUsage - 2.8, baseUsage + 2.8),

    rolling_3_mean: random(baseUsage - 1.0, baseUsage + 1.0),
    rolling_7_mean: random(baseUsage - 1.3, baseUsage + 1.3),
    rolling_14_mean: random(baseUsage - 1.5, baseUsage + 1.5),
    rolling_30_mean: random(baseUsage - 1.8, baseUsage + 1.8),
    rolling_60_mean: random(baseUsage - 2.0, baseUsage + 2.0),

    rolling_7_std: random(0.8, 2.4),
    rolling_30_std: random(1.0, 3.2),

    energy_change_1: random(-1.8, 1.8),
    energy_change_7: random(-2.5, 2.5),
    rolling_mean_gap: random(-2.2, 2.2),

    temperatureMax: random(24, 38),
    temperatureMin: random(12, 23),
    temperatureHigh: random(25, 39),
    temperatureLow: random(10, 22),
    humidity: random(0.45, 0.85),
    windSpeed: random(4, 18),
    pressure: random(1005, 1026),
    cloudCover: random(0.1, 0.9),
    visibility: random(6, 10),
    uvIndex: random(2, 9),
    dewPoint: random(5, 18),
    is_holiday: 0,
  };
};

function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [email, setEmail] = useState("toufique@test.com");
  const [password, setPassword] = useState("test12345");
  const [prediction, setPrediction] = useState(null);
  const [history, setHistory] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const authHeaders = {
    Authorization: `Bearer ${token}`,
  };

  const chartData = history
    .slice()
    .reverse()
    .map((item, index) => ({
      name: `F${index + 1}`,
      energy: item.predicted_energy_kwh,
      dailyCost: item.estimated_cost_usd,
      monthlyCost: Number((item.estimated_cost_usd * 30).toFixed(2)),
      carbon: item.carbon_emission_kg,
    }));

  const avgEnergy =
    history.length > 0
      ? (
          history.reduce((sum, item) => sum + item.predicted_energy_kwh, 0) /
          history.length
        ).toFixed(2)
      : "--";

  const avgDailyCost =
    history.length > 0
      ? (
          history.reduce((sum, item) => sum + item.estimated_cost_usd, 0) /
          history.length
        ).toFixed(2)
      : "--";

  const avgMonthlyCost =
    history.length > 0 ? (Number(avgDailyCost) * 30).toFixed(2) : "--";

  const avgCarbon =
    history.length > 0
      ? (
          history.reduce((sum, item) => sum + item.carbon_emission_kg, 0) /
          history.length
        ).toFixed(2)
      : "--";

  const latestRisk = history.length > 0 ? history[0].peak_risk : "--";

  const login = async () => {
    try {
      setLoading(true);
      setMessage("");

      const res = await axios.post(`${API}/auth/login`, {
        email: email.trim(),
        password: password.trim(),
      });

      localStorage.setItem("token", res.data.access_token);
      setToken(res.data.access_token);
      setMessage("Login successful.");
    } catch (error) {
      console.error("LOGIN ERROR:", error);
      setMessage(
        error.response?.data?.detail ||
          "Login failed. Please check backend server and credentials."
      );
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken("");
    setPrediction(null);
    setHistory([]);
    setMessage("Logged out.");
  };

  const loadHistory = async () => {
    try {
      const res = await axios.get(`${API}/forecast/history`, {
        headers: authHeaders,
      });

      setHistory(res.data.history || []);
    } catch (error) {
      console.error("HISTORY ERROR:", error);
      setMessage("Could not load history. Please login again.");
    }
  };

  const generateForecast = async () => {
    try {
      setLoading(true);
      setMessage("");

      const dynamicInput = createForecastInput();

      const res = await axios.post(`${API}/predict`, dynamicInput, {
        headers: authHeaders,
      });

      const enrichedPrediction = {
        ...res.data,
        monthly_cost_usd: Number((res.data.estimated_cost_usd * 30).toFixed(2)),
        monthly_carbon_kg: Number((res.data.carbon_emission_kg * 30).toFixed(2)),
      };

      setPrediction(enrichedPrediction);
      setMessage("New forecast generated with dynamic usage data.");
      await loadHistory();
    } catch (error) {
      console.error("FORECAST ERROR:", error);
      setMessage(
        error.response?.data?.detail ||
          "Forecast failed. Please login again or check backend."
      );
    } finally {
      setLoading(false);
    }
  };

  const downloadCSV = async () => {
    try {
      const res = await axios.get(`${API}/export/csv`, {
        headers: authHeaders,
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");

      link.href = url;
      link.setAttribute("download", "smart_energy_report.csv");
      document.body.appendChild(link);
      link.click();
      link.remove();

      setMessage("CSV report downloaded.");
    } catch (error) {
      console.error("CSV ERROR:", error);
      setMessage("CSV export failed. Please login again.");
    }
  };

  const downloadPDF = async () => {
    try {
      const res = await axios.get(`${API}/export/pdf`, {
        headers: authHeaders,
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");

      link.href = url;
      link.setAttribute("download", "smart_energy_report.pdf");
      document.body.appendChild(link);
      link.click();
      link.remove();

      setMessage("PDF report downloaded.");
    } catch (error) {
      console.error("PDF ERROR:", error);
      setMessage("PDF export failed. Please login again.");
    }
  };

  useEffect(() => {
    if (token) {
      loadHistory();
    }
  }, [token]);

  if (!token) {
    return (
      <div className="auth-page">
        <div className="auth-card">
          <div className="login-header">
            <div className="login-badge">
              Enterprise AI • Smart Grid • Energy Analytics
            </div>

            <h1 className="login-title">
              Smart Energy
              <span>Forecasting Platform</span>
            </h1>

            <p className="login-subtitle">
              Secure AI-powered energy forecasting, sustainability analytics,
              carbon monitoring, optimization insights, and intelligent decision
              support.
            </p>
          </div>

          <label>Email Address</label>
          <input
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your email"
          />

          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
          />

          <button onClick={login} disabled={loading}>
            {loading ? "Signing In..." : "Sign In"}
          </button>

          {message && <p className="status-message">{message}</p>}
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <header className="hero">
        <div className="hero-content">
          <div className="hero-badge">
            Enterprise AI • Smart Grid Intelligence • Energy Analytics
          </div>

          <h1>
            Smart Energy Forecasting &
            <span className="highlight"> Optimization Platform</span>
          </h1>

          <p className="subtitle">
            Industrial-grade machine learning platform for energy forecasting,
            sustainability analytics, carbon footprint monitoring, intelligent
            optimization, historical reporting, and enterprise decision support.
          </p>

          <div className="hero-stats">
            <div className="stat-box">
              <span>AI Model</span>
              <strong>Random Forest</strong>
            </div>

            <div className="stat-box">
              <span>Accuracy</span>
              <strong>85.93%</strong>
            </div>

            <div className="stat-box">
              <span>Platform</span>
              <strong>SaaS Ready</strong>
            </div>

            <div className="stat-box">
              <span>Forecasting</span>
              <strong>Real-Time</strong>
            </div>
          </div>
        </div>

        <div className="hero-actions">
          <button className="logout-btn" onClick={logout}>
            Logout
          </button>
        </div>
      </header>

      {message && <div className="status-banner">{message}</div>}

      <section className="action-row">
        <button onClick={generateForecast} disabled={loading}>
          {loading ? "Processing..." : "Generate Forecast"}
        </button>

        <button onClick={loadHistory} disabled={loading}>
          Load Forecast History
        </button>

        <button onClick={downloadCSV}>Export CSV</button>

        <button onClick={downloadPDF}>Export PDF</button>
      </section>

      <section className="kpi-grid">
        <div className="kpi-card primary">
          <p>Latest Forecast</p>
          <h2>
            {prediction
              ? `${prediction.predicted_energy_kwh} kWh`
              : history[0]
              ? `${history[0].predicted_energy_kwh} kWh`
              : "--"}
          </h2>
          <span>Advanced Random Forest</span>
        </div>

        <div className="kpi-card">
          <p>Average Energy</p>
          <h2>{avgEnergy} kWh</h2>
          <span>Based on saved forecast history</span>
        </div>

        <div className="kpi-card">
          <p>Average Daily Cost</p>
          <h2>${avgDailyCost}</h2>
          <span>Estimated daily energy cost</span>
        </div>

        <div className="kpi-card">
          <p>Average Monthly Cost</p>
          <h2>${avgMonthlyCost}</h2>
          <span>Latest risk: {latestRisk}</span>
        </div>
      </section>

      {history.length > 0 && (
        <section className="charts-grid">
          <div className="chart-card">
            <h3>Energy Forecast Trend</h3>
            <ResponsiveContainer width="100%" height={280}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="energy" strokeWidth={3} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-card">
            <h3>Cost & Carbon Analytics</h3>
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="monthlyCost" />
                <Bar dataKey="carbon" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>
      )}

      <section className="panel">
        <h3>Forecast History</h3>

        {history.length === 0 ? (
          <p className="empty-state">
            No forecast history available yet. Generate a forecast to begin
            tracking.
          </p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Energy</th>
                <th>Daily Cost</th>
                <th>Monthly Cost</th>
                <th>Carbon</th>
                <th>Risk</th>
              </tr>
            </thead>

            <tbody>
              {history.map((item) => {
                const monthlyCost = Number(
                  (item.estimated_cost_usd * 30).toFixed(2)
                );

                return (
                  <tr key={item.id}>
                    <td>{String(item.created_at).replace("T", " ").slice(0, 19)}</td>
                    <td>{item.predicted_energy_kwh} kWh</td>
                    <td>${item.estimated_cost_usd}</td>
                    <td>${monthlyCost}</td>
                    <td>{item.carbon_emission_kg} kg</td>
                    <td>{item.peak_risk}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </section>

      <footer>
        Smart Energy Forecasting & Optimization Platform
        <br />
        Developed by Toufique Hasan
      </footer>
    </div>
  );
}

export default App;