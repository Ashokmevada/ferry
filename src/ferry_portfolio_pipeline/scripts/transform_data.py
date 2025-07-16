import boto3
import pandas as pd
from io import StringIO
from ferry_portfolio_pipeline.config.settings import CONFIG
from ferry_portfolio_pipeline.logging.logger import logging as logger
from ferry_portfolio_pipeline.exception import CustomException

def read_csv_from_s3(bucket: str, key: str) -> pd.DataFrame:
    try:
        logger.info(f"⬇️ Reading file from S3: s3://{bucket}/{key}")
        s3 = boto3.client("s3")
        obj = s3.get_object(Bucket=bucket, Key=key)
        data = obj['Body'].read().decode('utf-8')
        df = pd.read_csv(StringIO(data))
        logger.info(f"✅ Successfully loaded {len(df)} rows.")
        return df
    except Exception as e:
        logger.error(f"❌ Error reading from S3: {e}")
        raise CustomException(e)

def upload_df_to_s3(df: pd.DataFrame, bucket: str, key: str):
    try:
        logger.info(f"⬆️ Uploading DataFrame to S3: s3://{bucket}/{key}")
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        s3 = boto3.client("s3")
        s3.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())
        logger.info("✅ Upload successful.")
    except Exception as e:
        logger.error(f"❌ Error uploading to S3: {e}")
        raise CustomException(e)

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    try:
        logger.info("🔄 Transforming data...")
        # Example transformation: add a new column 'processed' with True
        df = df.drop(columns=['_id'])
        df[['Year', 'Month', 'Day', 'Hour']] = pd.to_datetime(df['Timestamp']).apply(
        lambda x: pd.Series([x.year, x.month, x.day, x.hour]))
        df = df.drop(columns=['Timestamp'])
        logger.info("✅ Data transformation complete.")
        return df
    except Exception as e:
        logger.error(f"❌ Error during data transformation: {e}")
        raise CustomException(e)

def main():
    bucket = CONFIG["s3"]["bucket"]
    input_key = CONFIG["s3"]["key"]
    output_key = CONFIG["s3"]["output_key"]

    try:
        df = read_csv_from_s3(bucket, input_key)
        df_transformed = transform_data(df)
        upload_df_to_s3(df_transformed, bucket, output_key)
    except CustomException as e:
        logger.error(f"🚨 Pipeline failed: {e}")

if __name__ == "__main__":
    main()
