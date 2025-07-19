from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import subprocess
from ferry_portfolio_pipeline.scripts.extract_data import run_extraction
import os

import logging # Import logging to capture stderr

# Get the Airflow task logger
log = logging.getLogger(__name__)

# def run_dvc_add(data_path):

#     print("Hello")

#     log.info(f"Checking if file exists: {data_path}")
#     if not os.path.exists(data_path):
#         log.error(f"File DOES NOT exist at: {data_path}. DVC add will fail.")
#         # You might want to raise an AirflowException here or handle differently
#         raise FileNotFoundError(f"Data file not found: {data_path}")

#     log.info(f"Attempting to run: dvc add {data_path}")
#     try:
#         # Capture stdout and stderr
#         result = subprocess.run(
#             ["dvc", "add", data_path],
#             check=True,
#             capture_output=True, # Capture stdout and stderr
#             text=True # Decode stdout/stderr as text
#         )
#         log.info(f"DVC add successful. Stdout: {result.stdout}")
#     except subprocess.CalledProcessError as e:
#         log.error(f"DVC add failed with exit code {e.returncode}")
#         log.error(f"Stderr: {e.stderr}")
#         log.error(f"Stdout: {e.stdout}")
#         # Re-raise the exception so Airflow marks the task as failed
#         raise e
#     except FileNotFoundError as e: # This handles if 'dvc' command itself is not found
#         log.error(f"Command not found. Is DVC installed and in PATH? Error: {e}")
#         raise e
def run_dvc_add():
    data_path = "/opt/airflow/artifacts/ferry_raw.csv"
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"{data_path} not found!")
    
    print("File exists?", os.path.exists(data_path), data_path)

    
    subprocess.run(["dvc", "add", data_path], check=True)


# 3. DVC repro task
def run_dvc_repro():

    subprocess.run(["dvc", "repro"], check=True, cwd="/opt/airflow")

    

def run_dvc_push():
    subprocess.run(["dvc", "push"], check=True, cwd="/opt/airflow")
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

    dvc_push_task = PythonOperator(
    task_id='dvc_push_to_remote',
    python_callable=run_dvc_push
    )

# Chain tasks with push at the end
extract_task >> dvc_add_task >> dvc_repro_task >> dvc_push_task
