import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ferry_portfolio_pipeline.config.settings import CONFIG
from ferry_portfolio_pipeline.logging.logger import logging as logger
import boto3
import io
from io import StringIO
import joblib # <-- Add this import'
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="/app/.env")  # make sure path matches the mount


from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=300_000, key="data_refresh")  # 5 minutes

# Set Streamlit page config
st.set_page_config(
    page_title="Ferry Sales & Revenue Dashboard",
    layout="wide"
)

logger.info("🚀 Starting Ferry Sales & Revenue Executive Dashboard script")

# S3 setup
bucket = CONFIG["s3"]["bucket"]
output_key = CONFIG["s3"]["output_key"]
model_key = CONFIG["s3"]["model_key"]

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION"),
)

# Load data from S3
logger.info(f"⬇️ Fetching processed data from S3 key: {output_key}")
print(f"⬇️ Fetching processed data from S3 key: {os.getenv('AWS_ACCESS_KEY_ID')}")

obj = s3.get_object(Bucket=bucket, Key=output_key)
data = obj['Body'].read().decode('utf-8')
df = pd.read_csv(StringIO(data))

# Load model from S3
logger.info(f"⬇️ Fetching model from S3 key: {model_key}")
obj = s3.get_object(Bucket=bucket, Key=model_key)
model = joblib.load(io.BytesIO(obj['Body'].read()))

# Preprocess data
df['Date'] = pd.to_datetime(df['Date'])
df_date = df.groupby(['Date']).sum()[['Sales Count','Redemption Count']]
df = df_date.resample('ME').sum()[['Sales Count']].reset_index()
df = df[df['Date'] >= '2023-01-01']

# Forecasting
future = model.make_future_dataframe(periods=len(df), freq='M')
forecast = model.predict(future)

# Filter forecast to next 10 months
start_date = pd.Timestamp.today().replace(day=1) + pd.DateOffset(months=1)
end_date = start_date + pd.DateOffset(months=10)
forecast = forecast[(forecast['ds'] >= start_date) & (forecast['ds'] <= end_date)]

# Revenue calculations
ticket_price = 8.0
df['Revenue'] = df['Sales Count'] * ticket_price
forecast['Revenue'] = forecast['yhat'] * ticket_price

# KPI calculation
def get_kpis(df, forecast):
    kpis = {}
    last_month = df['Date'].max()
    last_data = df[df['Date'] == last_month]
    kpis['this_month_sales'] = last_data['Sales Count'].iloc[0]
    kpis['this_month_revenue'] = last_data['Revenue'].iloc[0]
    kpis['this_month_label'] = f"Latest ({last_month.strftime('%b %Y')})"
    
    next_month_forecast = forecast.iloc[0]
    kpis['next_month_sales'] = int(next_month_forecast['yhat'])
    kpis['next_month_revenue'] = next_month_forecast['Revenue']
    
    if len(df) >= 2:
        prev_month = df.iloc[-2]
        current_month = df.iloc[-1]
        kpis['prev_month_sales'] = prev_month['Sales Count']
        kpis['prev_month_revenue'] = prev_month['Revenue']
        kpis['sales_growth'] = ((current_month['Sales Count'] - prev_month['Sales Count']) / prev_month['Sales Count']) * 100
        kpis['revenue_growth'] = ((current_month['Revenue'] - prev_month['Revenue']) / prev_month['Revenue']) * 100
    else:
        kpis['prev_month_sales'] = kpis['this_month_sales']
        kpis['prev_month_revenue'] = kpis['this_month_revenue']
        kpis['sales_growth'] = 0
        kpis['revenue_growth'] = 0
    
    kpis['forecast_sales_change'] = ((kpis['next_month_sales'] - kpis['this_month_sales']) / kpis['this_month_sales']) * 100
    kpis['forecast_revenue_change'] = ((kpis['next_month_revenue'] - kpis['this_month_revenue']) / kpis['this_month_revenue']) * 100
    return kpis

kpis = get_kpis(df, forecast)

# Display KPIs in Streamlit
st.title("🚤 Ferry Sales & Revenue Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric(label=f"Current Month Sales ({kpis['this_month_label']})", value=f"{kpis['this_month_sales']:,}", delta=f"{kpis['sales_growth']:+.1f}%")
col2.metric(label="Next Month Forecast Sales", value=f"{kpis['next_month_sales']:,}", delta=f"{kpis['forecast_sales_change']:+.1f}%")
col3.metric(label="Sales Revenue Growth", value=f"${kpis['this_month_revenue']:,.0f}", delta=f"{kpis['revenue_growth']:+.1f}%")

col4, col5, col6 = st.columns(3)
col4.metric(label="Current Month Revenue", value=f"${kpis['this_month_revenue']:,.0f}")
col5.metric(label="Next Month Forecast Revenue", value=f"${kpis['next_month_revenue']:,.0f}", delta=f"{kpis['forecast_revenue_change']:+.1f}%")
col6.metric(label="Revenue per Ticket", value=f"${kpis['this_month_revenue']/kpis['this_month_sales']:.2f}")

# Plot charts using Plotly
fig = make_subplots(
    rows=2, cols=1,
    subplot_titles=["Ferry Sales Forecast", f"Ferry Revenue Forecast - Monthly Data (Ticket Price: ${ticket_price} CAD)"]
)

# Sales forecast line
fig.add_trace(go.Scatter(
    x=df['Date'], y=df['Sales Count'],
    mode='lines+markers+text',
    name='Actual Sales',
    text=df['Sales Count'],
    textposition='top center'
), row=1, col=1)

fig.add_trace(go.Scatter(
    x=forecast['ds'], y=forecast['yhat'],
    mode='lines+markers+text',
    name='Forecast Sales',
    text=forecast['yhat'].round(0),
    textposition='top center'
), row=1, col=1)

# Revenue forecast line
fig.add_trace(go.Scatter(
    x=df['Date'], y=df['Revenue'],
    mode='lines+markers+text',
    name='Actual Revenue',
    text=df['Revenue'].round(0),
    textposition='top center'
), row=2, col=1)

fig.add_trace(go.Scatter(
    x=forecast['ds'], y=forecast['Revenue'],
    mode='lines+markers+text',
    name='Forecast Revenue',
    text=forecast['Revenue'].round(0),
    textposition='top center'
), row=2, col=1)

fig.update_layout(
    height=800,
    width=1200,
    showlegend=True,
    template="plotly_white",
    margin=dict(l=40, r=40, t=80, b=40)
)

st.plotly_chart(fig, use_container_width=True)
