# Toronto Island Park Ferry Ticket Sales and Redemption Forecasting

## Project Overview

This project focuses on forecasting ferry ticket sales and redemptions for Toronto Island Park ferries using near real-time data collected at 15-minute intervals. Accurate forecasting of ticket sales and redemption volumes is critical to optimizing ferry operations, improving staff scheduling, and enhancing passenger experience.

## Business Problem

Toronto Island Park ferries face fluctuating passenger demand throughout the day. Without reliable forecasts of ticket sales and redemption counts, ferry operators struggle to:

- Efficiently allocate staff at ticket counters and boarding gates
- Schedule the appropriate number of ferry trips and vessel capacity
- Minimize passenger wait times and avoid overcrowding

## Importance of Forecasting

Forecasting ferry ticket sales and redemptions enables proactive operational planning instead of reactive decision-making. This leads to better alignment of ferry service capacity with passenger demand, improved operational efficiency, and a more pleasant experience for passengers.

## Project Goals

- Develop accurate time-series forecasting models for ticket sales and redemptions at 15-minute intervals
- Provide actionable insights for staffing and ferry scheduling based on forecasted demand
- Automate data ingestion, transformation, and forecasting workflows for real-time updates
- Create interactive dashboards that visualize forecasts and historical data for operational decision-makers

## Data Description

The dataset consists of:

- Timestamped records at 15-minute intervals
- Number of tickets sold
- Number of tickets redeemed (used to board the ferry)

## Methodology

1. **Data Exploration and Preprocessing:**  
   Analyze data trends, seasonality, and clean the dataset for modeling.

2. **Feature Engineering:**  
   Include time-based features (hour of day, day of week), holidays, and other relevant factors.

3. **Model Development:**  
   Experiment with classical and machine learning time series models (ARIMA, Prophet, LSTM, etc.) to forecast ticket sales and redemptions.

4. **Evaluation:**  
   Assess model accuracy using metrics such as RMSE and MAE.

5. **Automation:**  
   Use Apache Airflow to automate data pipelines and forecasting workflows.

6. **Visualization:**  
   Build Power BI dashboards that refresh automatically to present forecasts and KPIs.

## Tools and Technologies

- Python (pandas, scikit-learn, statsmodels, Prophet)
- Apache Airflow for pipeline orchestration
- Cloud SQL database (e.g., Supabase or AWS RDS)
- Streamlit or Power BI for dashboarding
- GitHub Actions for CI/CD

## Expected Outcomes

- Reliable forecasts of ferry ticket sales and redemptions at granular time intervals  
- Optimized staffing and ferry scheduling recommendations  
- Reduced wait times and improved passenger flow management  
- A fully automated, scalable forecasting pipeline with live dashboard updates

---

## Getting Started

1. Clone the repository  
2. Install dependencies via `pip install -r requirements.txt` or `pip install -e .`  
3. Configure database and Airflow connections  
4. Run data extraction, transformation, and forecasting scripts  
5. Access the Power BI dashboard connected to your cloud database

---

## Contact

For questions or feedback, please contact Ashok Mevada at ashokmevada18@gmail.com

---

*This project aims to contribute to sustainable and efficient ferry operations at Toronto Island Park through data-driven forecasting and analytics.*

📌 Why Install Airflow with Constraints?
To ensure a stable and compatible setup, we install Apache Airflow using an officially maintained constraints file. This guarantees that all dependencies are locked to versions that are tested and supported with the selected Airflow version.


AIRFLOW_VERSION=2.8.2
PYTHON_VERSION="$(python --version | cut -d ' ' -f 2 | cut -d '.' -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
✅ Benefits:
Avoids version conflicts

Ensures reliable DAG execution

Reproducible and production-ready installation.
