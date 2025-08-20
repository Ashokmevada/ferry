from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import subprocess
from ferry_portfolio_pipeline.scripts.extract_data import run_extraction
import os
import logging # Import logging to capture stderr

# Get the Airflow task logger
log = logging.getLogger(__name__)

# Re-enable and modify the run_dvc_add function
def run_dvc_add():
    data_path = "/opt/airflow/artifacts/ferry_raw.csv"

    log.info(f"Checking if file exists: {data_path}")
    if not os.path.exists(data_path):
        log.error(f"File DOES NOT exist at: {data_path}. DVC add will fail.")
        raise FileNotFoundError(f"Data file not found: {data_path}")

    log.info(f"Attempting to run: dvc add {data_path}")
    try:
        # Capture stdout and stderr
        result = subprocess.run(
            ["dvc", "add", data_path],
            check=True, # This will raise CalledProcessError if returncode is non-zero
            capture_output=True, # Capture stdout and stderr
            text=True # Decode stdout/stderr as text
        )
        log.info(f"DVC add successful. Stdout: {result.stdout}")
        # If DVC add succeeds, there's usually not much in stderr unless it's warnings.
        if result.stderr:
            log.warning(f"DVC add had stderr output: {result.stderr}")
    except subprocess.CalledProcessError as e:
        log.error(f"DVC add failed with exit code {e.returncode}")
        log.error(f"Stderr: {e.stderr}") # <--- This is what you need!
        log.error(f"Stdout: {e.stdout}") # <--- This might also contain useful info!
        # Re-raise the exception so Airflow marks the task as failed
        raise e
    except FileNotFoundError as e: # This handles if 'dvc' command itself is not found
        log.error(f"Command 'dvc' not found. Is DVC installed and in PATH? Error: {e}")
        raise e

# 3. DVC repro task
def run_dvc_repro():
    log.info("Attempting to run: dvc repro")
    try:
        result = subprocess.run(
            ["dvc", "repro"],
            check=True,
            cwd="/opt/airflow",
            capture_output=True,
            text=True
        )
        log.info(f"DVC repro successful. Stdout: {result.stdout}")
        if result.stderr:
            log.warning(f"DVC repro had stderr output: {result.stderr}")
    except subprocess.CalledProcessError as e:
        log.error(f"DVC repro failed with exit code {e.returncode}")
        log.error(f"Stderr: {e.stderr}")
        log.error(f"Stdout: {e.stdout}")
        raise e
    except FileNotFoundError as e:
        log.error(f"Command 'dvc' not found. Is DVC installed and in PATH? Error: {e}")
        raise e

def run_dvc_push():
    log.info("Attempting to run: dvc push")
    try:
        result =subprocess.run(
            ["dvc", "push"],
            check=True,
            cwd="/opt/airflow",
            capture_output=True,
            text=True
        )
        log.info(f"DVC push successful. Stdout: {result.stdout}")
        if result.stderr:
            log.warning(f"DVC push had stderr output: {result.stderr}")
    except subprocess.CalledProcessError as e:
        log.error(f"DVC push failed with exit code {e.returncode}")
        log.error(f"Stderr: {e.stderr}")
        log.error(f"Stdout: {e.stdout}")
        raise e
    except FileNotFoundError as e:
        log.error(f"Command 'dvc' not found. Is DVC installed and in PATH? Error: {e}")
        raise e


from ferry_portfolio_pipeline.config.settings import CONFIG
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