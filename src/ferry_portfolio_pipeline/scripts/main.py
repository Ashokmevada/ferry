from ferry_portfolio_pipeline.config.settings import CONFIG
from ferry_portfolio_pipeline.config.common_utils import load_params
from ferry_portfolio_pipeline.config.common_utils import read_csv_from_s3
from ferry_portfolio_pipeline.scripts.evaluator import evaluate_prophet_models
from ferry_portfolio_pipeline.scripts.model_training import train_final_model
from ferry_portfolio_pipeline.logging.logger import logging as logger
import pickle
import boto3
import os

def save_model_locally(model, local_path: str):

    with open(local_path , "wb") as f:
        pickle.dump(model, f)
    logger.info(f"✅ Model saved locally at {local_path}")

def upload_model_to_s3(local_path , bucket: str, key: str):

    s3 = boto3.client("s3")
    s3.upload_file(local_path , bucket, key)
    logger.info(f"✅ Model uploaded to S3 at {key}")

def main():
    try:
        bucket = CONFIG["s3"]["bucket"]
        train_key = CONFIG["s3"]["train_output_key"]
        prophet_config = load_params()["prophet"]
        model_key = CONFIG["s3"]["model_key"]
        local_model_path = CONFIG["model_path"]


        logger.info("📥 Reading training data...")
        train_df = read_csv_from_s3(bucket, train_key)

        logger.info("🔎 Performing model evaluation...")
        best_params, results_df = evaluate_prophet_models(train_df, prophet_config)

        logger.info("🏗 Training final model...")
        model = train_final_model(train_df, best_params, prophet_config)

        logger.info("💾 Saving model locally...")
        save_model_locally(model, local_model_path)

        logger.info("☁ Uploading model to S3...")
        upload_model_to_s3(local_model_path, bucket, model_key)

        logger.info("✅ Model saved and uploaded successfully!")



        # Optional: save model, results_df, or generate forecast
    except Exception as e:
        logger.error(f"🚨 Pipeline failed: {e}")

if __name__ == "__main__":
    main()
