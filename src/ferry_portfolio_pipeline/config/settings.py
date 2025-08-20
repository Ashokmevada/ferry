import os

CONFIG = {
    "s3": {
        "bucket": "ashok-ferry-data-bucket",               # S3 bucket name
        "key": "raw_data/raw.csv",
        "output_key": "transformed_data/transformed.csv",
        "train_output_key" : "transformed_data/train.csv",
        "test_output_key": "transformed_data/test.csv",
        "model_key" : "model/prophet_model.pkl",     # Path inside the bucket where the file will be stored
        "region": "us-east-1",      
                                        # (Optional) AWS region of the bucket
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),     # Your AWS IAM access key
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),  # Your AWS IAM secret key
    },
    "transformed_df_path": "artifacts/transformed_data.csv",  # Local path to save the transformed DataFrame
    "train_df_path": "artifacts/train.csv",  # Local path to save the
    "test_df_path": "artifacts/test.csv",    # Local path to save the test DataFrame
    "cut_off_date": "2024-01-01", # Start date for the data
    "model_path": "artifacts/prophet_model.pkl",  # Local path to save the trained model
      
}