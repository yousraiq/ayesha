import requests
import pandas as pd
import boto3
import os
from datetime import datetime

# API endpoint
API_URL = "https://restcountries.com/v3.1/all"

# AWS S3 configuration
S3_BUCKET = "cde-capstone"  # Replace with your bucket name
AWS_ACCESS_KEY = "AKIAU6VTTFBOJVZS6FWM"  # Replace with your access key
AWS_SECRET_KEY = "RCHivpHeBgvtYnT5m+AyScvz4jhGQ2RSxS/DhpUl"  # Replace with your secret key
S3_REGION = "ap-south-1"  # Replace with your AWS region

def fetch_country_data():
    """Fetches data from the Country REST API."""
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

def save_to_parquet(data, file_path):
    """Saves data to a Parquet file."""
    df = pd.DataFrame(data)
    df.to_parquet(file_path, engine="pyarrow", index=False)

def upload_to_s3(file_path, s3_bucket, s3_key):
    """Uploads a file to S3."""
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=S3_REGION,
    )
    s3.upload_file(file_path, s3_bucket, s3_key)
    print(f"File uploaded to S3: {s3_bucket}/{s3_key}")

def main(api_url, s3_bucket, s3_folder):
    """Main function to fetch data, save to Parquet, and upload to S3."""
    # Fetch data
    print("Fetching country data...")
    country_data = fetch_country_data(api_url)

    # Save to local Parquet file
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"countries_{timestamp}.parquet"
    save_to_parquet(country_data, file_name)
    print(f"Data saved locally as {file_name}")

    # Upload to S3
    s3_key = f"{s3_folder}/{file_name}"
    upload_to_s3(file_name, s3_bucket, s3_key)

    # Clean up local file
    os.remove(file_name)
    print("Local file removed after upload.")

if __name__ == "__main__":
    # You can set the default values here
    api_url = "https://restcountries.com/v3.1/all"
    main(api_url, S3_BUCKET, "raw-data")