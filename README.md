# open-meteo-project

### Ideas:
* Forecast running daily/hourly
* Archiving forcast data up to 30 days
* Comparing stored forecast data with historical endpoint/forcast current vs achived forecast


# Polish Weather Data Engineering Project
A data engineering project focused on collecting, storing, and visualizing weather forecast data for cities across Poland using the Open-Meteo API.

## Project Overview

This project builds a complete data pipeline to:
- Fetch weather forecast data from Open-Meteo API for Polish cities
- Store historical forecasts in PostgreSQL
- Orchestrate data collection with Apache Airflow
- Visualize weather patterns and forecast accuracy

## Architecture

```
Open-Meteo API
      ↓
Python Scripts (SQLAlchemy)
      ↓
Apache Airflow (Main Machine) ← Orchestration
      ↓
PostgreSQL (Raspberry Pi 3) ← Data Storage
      ↓
Visualizations:
  - Power BI
  - Python (Streamlit/Plotly Dash)
  - Vega-Lite (Web Dashboard)
```

### Infrastructure Setup

**Main Machine:**
- Apache Airflow for orchestration
- Development environment
- Heavy computation tasks

**Raspberry Pi 3:**
- PostgreSQL database hosting
- Cron jobs for lightweight scheduled tasks
- Optional: Flask API for data serving

## Project Ideas

### 1. Forecast Accuracy Tracking
**Goal:** Measure how accurate weather forecasts are over time

**Implementation:**
- Store forecasts at different time horizons (1-day, 3-day, 7-day ahead)
- When actual weather arrives, compare against historical forecasts
- Calculate accuracy metrics (MAE, RMSE) for temperature, precipitation
- Visualize accuracy degradation over forecast horizon

**Questions to Answer:**
- How much does forecast accuracy drop between 1-day and 7-day predictions?
- Which cities have the most/least accurate forecasts?
- Which weather variables are hardest to predict (temperature vs precipitation)?

### 2. Regional Weather Patterns
**Goal:** Analyze weather variations across Polish regions

**Implementation:**
- Group cities by voivodeships (Pomorskie, Mazowieckie, Małopolskie, etc.)
- Track temperature gradients across the country
- Monitor precipitation patterns
- Visualize weather system movement

**Questions to Answer:**
- What's the typical temperature difference between northern and southern Poland?
- How do weather systems move across the country?
- Which regions experience the most weather variability?

### 3. Anomaly Detection
**Goal:** Identify unusual weather forecast changes

**Implementation:**
- Calculate baseline weather patterns for each city
- Flag forecasts that deviate significantly from historical norms
- Detect sudden forecast changes (e.g., temperature drop >10°C in 24h)
- Create alert system for extreme weather predictions

**Questions to Answer:**
- When are sudden weather changes forecasted?
- Which cities experience the most anomalies?
- Can we predict severe weather events early?

### 4. Forecast Change Tracking
**Goal:** Understand how forecasts evolve as we approach the actual date

**Implementation:**
- For a given future date, store forecasts made at T-7, T-5, T-3, T-1 days
- Track how predicted values change as time approaches
- Visualize forecast convergence
- Measure forecast stability

**Questions to Answer:**
- How much does tomorrow's forecast change between 7 days out and 1 day out?
- When do forecasts "settle" into their final values?
- Which variables stabilize earliest (temperature vs precipitation)?

## Technology Stack

### Data Collection
- **Python 3.x** - Primary programming language
- **Requests** - API calls to Open-Meteo
- **SQLAlchemy** - ORM and database operations
- **Pandas** - Data manipulation

### Storage
- **PostgreSQL** - Main database (hosted on Raspberry Pi)
- **SQLAlchemy Models** - Database schema definition

### Orchestration
- **Apache Airflow** - Workflow orchestration (main machine)
- **Cron** - Simple scheduling (Raspberry Pi fallback)
- Alternative: **Prefect** (lighter weight option)

### Visualization
- **Power BI** - Professional dashboards (Windows)
- **Streamlit** - Python-based interactive web apps
- **Plotly Dash** - Advanced Python dashboards
- **Vega-Lite** - Declarative web visualizations
- **Matplotlib/Seaborn** - Static analysis plots

## Database Schema (Draft)

### Table: `cities`
- `id` (PK)
- `name`
- `latitude`
- `longitude`
- `voivodeship`
- `population`

### Table: `weather_forecasts`
- `id` (PK)
- `city_id` (FK)
- `forecast_fetch_time` - When the forecast was retrieved
- `forecast_target_time` - The date/time being forecasted
- `forecast_horizon_hours` - How many hours ahead (24, 72, 168, etc.)
- `temperature_2m`
- `precipitation`
- `wind_speed_10m`
- `relative_humidity_2m`
- `pressure_msl`
- `cloud_cover`

### Table: `weather_actuals` (Optional)
- `id` (PK)
- `city_id` (FK)
- `observation_time`
- `temperature_2m`
- `precipitation`
- (Same fields as forecasts for comparison)

##  Implementation Roadmap

### Phase 1: MVP (Minimum Viable Pipeline)
- [ ] Set up PostgreSQL on Raspberry Pi
- [ ] Create database schema with SQLAlchemy
- [ ] Write Python script to fetch weather for one city
- [ ] Store data in PostgreSQL
- [ ] Verify data quality

### Phase 2: Scale Up
- [ ] Add all Polish cities to database
- [ ] Implement batch API calls for all cities
- [ ] Set up cron job on Raspberry Pi (or Airflow on main machine)
- [ ] Schedule regular data collection (every 3-6 hours)
- [ ] Add logging and error handling

### Phase 3: Orchestration
- [ ] Install Apache Airflow on main machine
- [ ] Create DAGs for data collection workflows
- [ ] Implement data quality checks
- [ ] Set up monitoring and alerts
- [ ] Add retry logic and failure handling

### Phase 4: Visualization
- [ ] Create basic exploratory analysis with Pandas
- [ ] Build Streamlit dashboard (or choose preferred tool)
- [ ] Implement forecast accuracy visualizations
- [ ] Create regional comparison views
- [ ] Design anomaly detection dashboard

### Phase 5: Advanced Features
- [ ] Implement forecast accuracy tracking
- [ ] Build anomaly detection models
- [ ] Create forecast change tracking
- [ ] Add regional pattern analysis
- [ ] Optimize query performance

##  Development Notes

### Open-Meteo API
- **Endpoint:** `https://api.open-meteo.com/v1/forecast`
- **No API key required** (free tier)
- **Rate limits:** Reasonable for personal projects
- **Coverage:** Excellent for European cities

### Example API Call
```python
import requests

params = {
    'latitude': 52.2297,  # Warsaw
    'longitude': 21.0122,
    'hourly': 'temperature_2m,precipitation,wind_speed_10m',
    'forecast_days': 7
}

response = requests.get('https://api.open-meteo.com/v1/forecast', params=params)
data = response.json()
```

### Raspberry Pi Considerations
- **Memory:** 1GB RAM - avoid running Airflow here
- **Storage:** Use external storage if collecting long-term data
- **Network:** Ensure stable connection for database hosting
- **Power:** Consider UPS for database reliability

### Data Collection Frequency
- **Recommended:** Every 3-6 hours
- **Reasoning:** Balances data granularity with API courtesy
- **Storage:** ~10-20 MB per day for all Polish cities (estimate)

## 🔧 Setup Instructions

### 1. Raspberry Pi Setup
```bash
# Install PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb weather_poland

# Configure for remote connections (edit postgresql.conf and pg_hba.conf)
```

### 2. Python Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install sqlalchemy psycopg2-binary requests pandas apache-airflow streamlit
```

### 3. Database Connection
```python
from sqlalchemy import create_engine

engine = create_engine('postgresql://user:password@raspberry_pi_ip:5432/weather_poland')
```

##  Resources

- [Open-Meteo API Documentation](https://open-meteo.com/en/docs)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Streamlit Documentation](https://docs.streamlit.io/)

##  Visualization Ideas

### Dashboard 1: Real-time Overview
- Current forecast for all major Polish cities
- Temperature map of Poland
- Precipitation radar
- Wind patterns

### Dashboard 2: Forecast Accuracy
- Accuracy metrics by city
- Accuracy degradation over time horizon
- Error distribution charts
- Best/worst performing cities

### Dashboard 3: Regional Analysis
- Regional temperature comparisons
- Precipitation patterns by voivodeship
- Weather system movement animations
- Seasonal trend analysis

### Dashboard 4: Anomaly Alerts
- Recent anomaly detections
- Historical anomaly frequency
- Extreme weather predictions
- Alert timeline

##  Contributing

This is a personal learning project, but ideas and suggestions are welcome!

##  License

Open for personal and educational use.

---

**Last Updated:** February 2026
**Status:** Planning Phase
**Next Steps:** Set up PostgreSQL on Raspberry Pi and create initial database schema