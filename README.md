# Toronto Island Ferry Sales & Revenue Forecasting  

## 📌 Project Overview  
This project focuses on forecasting **monthly ferry ticket sales and revenue** for Toronto Island ferries using historical data and advanced time-series models. Accurate forecasting of demand and revenue supports city planners, ferry operators, and tourism authorities in making strategic, data-driven decisions.  

---

## 🚢 Business Problem  
Toronto Island ferries experience strong seasonal fluctuations in passenger demand. Without reliable forecasts, operators and city officials face challenges in:  

- Allocating resources (staff, vessels, maintenance) efficiently  
- Optimizing ticket pricing and revenue strategies  
- Planning for tourism demand and visitor inflows  
- Supporting sustainability goals by reducing unnecessary trips  

---

## 📈 Importance of Forecasting  
Forecasting sales and revenue enables proactive planning instead of reactive responses. It ensures better capacity management, sustainable transportation policies, and optimized financial outcomes.  

---

## 🎯 Project Goals  
- Build accurate time-series forecasting models for ferry sales and revenue  
- Identify seasonal and trend patterns to guide decision-making  
- Automate data pipelines and model training for scalability  
- Provide interactive dashboards for real-time monitoring and insights  

---

## 📊 Data Description  
- **Source:** Toronto government open data portal  
- **Granularity:** Monthly ticket sales and revenue data  
- **Storage:** Raw and transformed data stored in AWS S3 and RDS  

---

## ⚙️ Methodology  
1. **Data Processing:** Cleaning and transformation with Python  
2. **Forecasting:** Prophet model with hyperparameter tuning (cross-validation, RMSE evaluation)  
3. **Infrastructure:** Automated workflows with Apache Airflow and DVC, containerized with Docker  
4. **Deployment:** Deployed on AWS ECS/ECR with GitHub Actions CI/CD  
5. **Visualization:** Streamlit dashboard with auto-refresh for continuous monitoring  

---

## 🛠️ Tools & Technologies  
- **Python** (pandas, Prophet, scikit-learn)  
- **Cloud:** AWS S3, RDS, ECS, ECR  
- **Workflow & Versioning:** Apache Airflow, DVC  
- **Containerization & CI/CD:** Docker, GitHub Actions  
- **Visualization:** Streamlit  

---

## ✅ Expected Outcomes  
- Reliable monthly forecasts of ferry sales and revenue  
- Seasonal demand insights for tourism and operations planning  
- Optimized scheduling, staffing, and pricing recommendations  
- Automated, scalable forecasting pipeline with live dashboards  

---

## 🚀 Getting Started  

1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/ferry-forecasting.git
   cd ferry-forecasting
   
2.Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure AWS and Airflow connections

4. Run data extraction, transformation, and forecasting scripts

5. Access the Streamlit dashboard for forecasts and KPIs

📬 Contact

For questions or feedback, please contact:

Ashok Mevada
📧 Email: ashokmevada18@gmail.com

🌐 Portfolio: ashokmevada.com
