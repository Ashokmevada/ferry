from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import subprocess

# 1. Your own extraction script
from ferry_portfolio_pipeline.scripts.extract_data import run_extraction

# 2. DVC add task
def run_dvc_add():
    data_path = "data/raw/data.csv"  # Change if your file is named differently
    subprocess.run(["dvc", "add", data_path], check=True)

# 3. DVC repro task
def run_dvc_repro():
    subprocess.run(["dvc", "repro", "transform"], check=True)

# Default DAG args
default_args = {
    'owner': 'ashok',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id='ferry_portfolio_etl',
    default_args=default_args,
    description='Extract data -> dvc add -> dvc repro (transform)',
    schedule_interval='*/5 * * * *',
    start_date=datetime(2024, 7, 1),
    catchup=False,
    tags=['portfolio', 'etl'],
) as dag:

    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=run_extraction
    )

    dvc_add_task = PythonOperator(
        task_id='dvc_add_data',
        python_callable=run_dvc_add
    )

    dvc_repro_task = PythonOperator(
        task_id='dvc_repro_transform',
        python_callable=run_dvc_repro
    )

    # Task chaining
    extract_task >> dvc_add_task >> dvc_repro_task
