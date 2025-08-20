import boto3
import pandas as pd
from io import StringIO
from ferry_portfolio_pipeline.config.settings import CONFIG
from ferry_portfolio_pipeline.logging.logger import logging as logger
from ferry_portfolio_pipeline.exception import CustomException
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
import os


def save_df_locally(df: pd.DataFrame, local_path: str):
    try:
        logger.info(f"💾 Saving DataFrame locally at: {local_path}")
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        df.to_csv(local_path, index=False)
        logger.info("✅ Local save successful.")
    except Exception as e:
        logger.error(f"❌ Error saving locally: {e}")
        raise CustomException(e)


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

def transform_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    try:
        logger.info("Transforming data...")
        
        # Drop the _id column as before
        df = df.drop(columns=['_id'])
        
        # Convert the 'Timestamp' column to datetime objects
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        
        # Extract date, year, month, day, and hour using the .dt accessor
        df['Date'] = df['Timestamp'].dt.date
        df['Year'] = df['Timestamp'].dt.year
        df['Month'] = df['Timestamp'].dt.month
        df['Day'] = df['Timestamp'].dt.day
        df['Hour'] = df['Timestamp'].dt.hour

        # Sorting should now work correctly because 'Date' contains date objects, not methods
        df = df.sort_values('Date')
        
        # Drop the original 'Timestamp' column
        df = df.drop(columns=['Timestamp'])
        
        # Resample the data
        df_2021 = df[df['Year'] >= 2021]
        
        # Make sure the index is a datetime index for resampling
        df_2021['Date'] = pd.to_datetime(df_2021['Date'])
        df_2021 = df_2021.set_index('Date')
        
        df_2021 = df_2021.resample('M').sum(numeric_only=True)[['Sales Count']]
        df_2021.reset_index(inplace=True)
        
        # Prepare data for Prophet
        df_2021.rename(columns={'Date': 'ds', 'Sales Count': 'y'}, inplace=True)
        
        # Split the data into training and test sets
        cut_off_date = pd.to_datetime(CONFIG["cut_off_date"])
        train_df = df_2021[df_2021['ds'] < cut_off_date].copy()
        test_df = df_2021[df_2021['ds'] >= cut_off_date].copy()

        logger.info("✅ Data transformation complete.")
        return df, train_df, test_df
        
    except Exception as e:
        logger.error(f"❌ Error during data transformation: {e}")
        # Assuming CustomException is defined to handle a single argument
        # as per your code's usage in other functions.
        raise CustomException(e)
def run_transformation():
    main()
    

def main():

    bucket = CONFIG["s3"]["bucket"]
    input_key = CONFIG["s3"]["key"]
    output_key = CONFIG["s3"]["output_key"]
    train_output_key = CONFIG["s3"]["train_output_key"]
    test_output_key = CONFIG["s3"]["test_output_key"]
    local_output_path = CONFIG["transformed_df_path"]
    local_train_output_path = CONFIG["train_df_path"]
    local_test_output_path  = CONFIG["test_df_path"]

    try:
        df = read_csv_from_s3(bucket, input_key)
        df_transformed, train_df, test_df = transform_data(df)
        
        # Save locally
        save_df_locally(df_transformed, local_output_path)
        save_df_locally(train_df, local_train_output_path)
        save_df_locally(test_df, local_test_output_path)


        # Upload to S3
        upload_df_to_s3(df_transformed, bucket, output_key)
        upload_df_to_s3(train_df, bucket, train_output_key)
        upload_df_to_s3(test_df, bucket, test_output_key)
    except CustomException as e:
        logger.error(f"🚨 Pipeline failed: {e}")

if __name__ == "__main__":
    main()
