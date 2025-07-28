# Use official Apache Airflow base image
FROM apache/airflow:2.8.1-python3.10

WORKDIR /opt/airflow

# Switch to root to install system packages
USER root

# Install git, curl, and DVC with S3 support
RUN apt-get update && \
    apt-get install -y git curl && \
    pip install --no-cache-dir dvc[s3] && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set up Git user (required for commits)
RUN git config --global user.email "ashok@example.com" && \
    git config --global user.name "Ashok Mevada"

# Switch to airflow user before installing Python packages
USER airflow
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy DAGs, plugins, source code, artifacts
COPY --chown=airflow:root airflow/dags/ /opt/airflow/dags/
COPY --chown=airflow:root airflow/plugins/ /opt/airflow/plugins/
COPY --chown=airflow:root src/ /opt/airflow/src/
COPY --chown=airflow:root artifacts/ /opt/airflow/Artifacts/

# PYTHONPATH for custom modules
ENV PYTHONPATH=/opt/airflow/src:$PYTHONPATH

# Create artifact directories
RUN mkdir -p \
    /opt/airflow/Artifacts/data_ingestion/feature_store \
    /opt/airflow/Artifacts/data_validation \
    /opt/airflow/Artifacts/model_trainer \
    /opt/airflow/Artifacts/model_evaluation \
    /opt/airflow/Artifacts/model_pusher && \
    chmod -R 777 /opt/airflow/Artifacts

# Switch back to root to initialize Git + DVC (must be done once)
USER root
RUN cd /opt/airflow && \
    git init && \
    dvc init --subdir && \
    git add . && \
    git commit -m "Initial Git and DVC setup"

# Switch back to airflow user for final runtime
USER airflow

# Default entrypoint
ENTRYPOINT ["airflow"]
CMD ["version"]
