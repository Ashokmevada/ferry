import yaml
import boto3
import pandas as pd
from io import StringIO
from ferry_portfolio_pipeline.exception import CustomException
from ferry_portfolio_pipeline.logging.logger import logging as logger

def load_params(path="params.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def read_csv_from_s3(bucket: str, key: str) -> pd.DataFrame:
    try:
        logger.info(f"⬇️ Reading file from s3://{bucket}/{key}")
        s3 = boto3.client("s3")
        obj = s3.get_object(Bucket=bucket, Key=key)
        df = pd.read_csv(StringIO(obj["Body"].read().decode("utf-8")))
        logger.info(f"✅ Loaded {len(df)} rows.")
        return df
    except Exception as e:
        logger.error(f"❌ Failed to read from S3: {e}")
        raise CustomException(e)
