# Use the official Airflow image as the base
FROM apache/airflow:2.9.1

# Install DVC.
# You might need to install additional system dependencies for dvc if using a specific remote storage (e.g., git, ssh, s3, gdrive, azure, etc.)
# For basic DVC with local Git repositories, this should be sufficient.
# We're installing it into the system site-packages for the Airflow user to access it easily.
USER airflow
RUN pip install --no-cache-dir "dvc[s3]" 

# Switch back to the airflow user

# You can add other dependencies here if needed for your DAGs
# RUN pip install --no-cache-dir pandas scikit-learn