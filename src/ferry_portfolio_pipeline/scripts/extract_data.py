import os
import requests
import pandas as pd
import boto3
from io import StringIO
from ferry_portfolio_pipeline.logging.logger import logging as logger
from ferry_portfolio_pipeline.exception import CustomException
from ferry_portfolio_pipeline.config.settings import CONFIG

# Temporary file path for DVC tracking
TEMP_DVC_FILE = ".dvc-temp/ferry_raw.csv"


def save_temp_for_dvc(df: pd.DataFrame, file_path: str):
    """Save DataFrame locally to a temp file (for DVC tracking)."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_csv(file_path, index=False)
        logger.info(f"✅ Saved temporary file for DVC: {file_path}")
    except Exception as e:
        logger.error(f"❌ Error saving local temp file: {e}")
        raise CustomException(e)


def upload_to_s3(df: pd.DataFrame, bucket: str, key: str):
    """Upload the DataFrame to AWS S3 as a CSV."""
    try:
        logger.info(f"🪣 Uploading file to S3: s3://{bucket}/{key}")
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)

        s3 = boto3.client("s3")
        s3.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())

        logger.info("✅ Successfully uploaded CSV to S3.")
    except Exception as e:
        logger.error(f"❌ Error uploading to S3: {e}")
        raise CustomException(e)


def get_ckan_data(package_id: str) -> pd.DataFrame:
    """Fetch ferry ticket count data from Toronto CKAN."""
    try:
        base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
        package_url = f"{base_url}/api/3/action/package_show"
        response = requests.get(package_url, params={"id": package_id})
        package = response.json()

        for resource in package["result"]["resources"]:
            if resource["datastore_active"]:
                search_url = f"{base_url}/api/3/action/datastore_search"
                records = []
                offset = 0
                limit = 1000

                while True:
                    params = {"id": resource["id"], "limit": limit, "offset": offset}
                    result = requests.get(search_url, params=params).json()["result"]
                    records.extend(result["records"])
                    offset += limit
                    if len(result["records"]) < limit:
                        break

                return pd.DataFrame(records)

        raise ValueError("No active datastore resource found.")
    except Exception as e:
        logger.error(f"❌ Error fetching CKAN data: {e}")
        raise CustomException(e)


def main():
    try:
        logger.info("🚀 Starting ferry data extraction pipeline...")
        df = get_ckan_data("toronto-island-ferry-ticket-counts")
        logger.info(f"📊 Retrieved {df.shape[0]} rows and {df.shape[1]} columns")

        # 1️⃣ Save temporary file for DVC tracking
        save_temp_for_dvc(df, TEMP_DVC_FILE)

        # 2️⃣ Upload to AWS S3
        upload_to_s3(
            df,
            bucket=CONFIG["s3"]["bucket"],  # e.g., "ashok-ferry-data-bucket"
            key=CONFIG["s3"]["key"]         # e.g., "ferry_raw/ferry_raw.csv"
        )

        # 3️⃣ Optional: delete temp file after tracking
        if os.path.exists(TEMP_DVC_FILE):
            os.remove(TEMP_DVC_FILE)
            logger.info("🧹 Removed temporary local file after upload.")

    except Exception as e:
        logger.error(f"🚨 Failed in extract_data pipeline: {e}")


if __name__ == "__main__":
    main()
