import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "ferry_portfolio_pipeline"

list_of_files = [
    # Existing structure
    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/scripts/__init__.py",
    f"src/{project_name}/scripts/extract_data.py",
    f"src/{project_name}/scripts/transform_data.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/settings.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/entity/config_entity.py",
    f"src/{project_name}/constants/__init__.py",
    f"src/{project_name}/logging/__init__.py",
    f"src/{project_name}/exception/__init__.py",
    f"src/{project_name}/cloud/__init__.py",
    ".env",
    "config/config.yaml",
    "params.yaml",
    "schema.yaml",
    "notebooks/eda.ipynb",
    "Dockerfile",
    "requirements.txt",
    "setup.py",
    "README.md",
    "test.py",

    # ---------------------------
    # Airflow-specific structure
    # ---------------------------
    "airflow/dags/__init__.py",
    "airflow/dags/ferry_pipeline_dag.py",        # your main DAG
    "airflow/plugins/__init__.py",               # for custom operators/hooks
    "airflow/logs/.gitkeep",                     # Airflow logs directory
    "airflow/config/airflow.cfg",                # airflow config (optional; can be generated)
    "airflow/docker/.gitkeep",                   # if running Airflow via Docker Compose
    "airflow/README.md",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file: {filename}")
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")
