# Use official Apache Airflow base image
FROM apache/airflow:2.8.1-python3.10

WORKDIR /opt/airflow

# Switch to root to install system packages
USER root
RUN apt-get update && apt-get install -y git curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt
COPY requirements.txt .

# Switch to airflow user before installing python packages
USER airflow
RUN pip install --no-cache-dir -r requirements.txt

# Copy DAGs and plugins as airflow user
COPY --chown=airflow:root airflow/dags/ /opt/airflow/dags/
COPY --chown=airflow:root airflow/plugins/ /opt/airflow/plugins/

# Copy the dvc configuration directory
# Removed redundant COPY .dvc/config as .dvc/ covers it
COPY --chown=airflow:root .dvc/ /opt/airflow/.dvc/

# Copy source code as airflow user
COPY --chown=airflow:root src/ /opt/airflow/src/

# Copy artifacts directory (assuming it contains ferry_raw.csv)
COPY --chown=airflow:root artifacts/ /opt/airflow/artifacts/

# Copy DVC.yaml file dvc staging task in DAG
COPY --chown=airflow:root dvc.yaml /opt/airflow/dvc.yaml

# Copy the params.yaml file for the model training task
COPY --chown=airflow:root params.yaml /opt/airflow/params.yaml

# ADD PYTHON PATH HERE:
ENV PYTHONPATH=/opt/airflow/src:$PYTHONPATH

# --- START: GIT INITIALIZATION FOR DVC ---
# Ensure we are in the WORKDIR for git operations
WORKDIR /opt/airflow

# Initialize Git repository
# DVC requires a Git repository to function correctly
RUN git init

# Configure Git user (required for commits)
# These values can be generic as they are for the container's internal git repo
RUN git config user.email "ashokmevada18@gmail.com" && \
    git config user.name "Ashok Mevada"

# Add and commit initial DVC files to the newly initialized Git repo
# This makes DVC recognize the directory as a DVC repository
# '|| true' ensures the build doesn't fail if there's nothing to commit (e.g., empty .dvc folder initially)
RUN git add .dvc/ && \
    git add artifacts/ && \
    git commit -m "Initial DVC repository setup in container" || true
# --- END: GIT INITIALIZATION FOR DVC ---
    
# Create artifact directories as airflow user (if they don't exist from COPY artifacts/)
# This ensures the necessary subdirectories for DVC artifacts are present and have correct permissions
RUN mkdir -p \
    /opt/airflow/Artifacts/data_ingestion/feature_store \
    /opt/airflow/Artifacts/data_validation \
    /opt/airflow/Artifacts/model_trainer \
    /opt/airflow/Artifacts/model_evaluation \
    /opt/airflow/Artifacts/model_pusher && \
    chmod -R 777 /opt/airflow/Artifacts

# Use airflow user for rest of the container
USER airflow

ENTRYPOINT ["airflow"]
CMD ["version"]