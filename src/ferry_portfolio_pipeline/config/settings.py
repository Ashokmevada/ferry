import os

CONFIG = {
    "s3": {
        "bucket": "ashok-ferry-data-bucket",               # S3 bucket name
        "key": "raw_data/raw.csv",
        "output_key": "transformed_data/transformed.csv",      # Path inside the bucket where the file will be stored
        "region": "us-east-1",                      # (Optional) AWS region of the bucket
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),     # Your AWS IAM access key
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),  # Your AWS IAM secret key
    }
}