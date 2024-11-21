import pandas as pd
import boto3
import os
from io import BytesIO

# AWS S3 configuration
S3_BUCKET = "cde-capstone"  # Replace with your bucket name
AWS_ACCESS_KEY = "AKIAU6VTTFBOJVZS6FWM"  # Replace with your access key
AWS_SECRET_KEY = "RCHivpHeBgvtYnT5m+AyScvz4jhGQ2RSxS/DhpUl"  # Replace with your secret key
S3_REGION = "ap-south-1"  # Replace with your AWS region

# File paths in S3
RAW_DATA_PATH = "raw-data/"  # Replace with raw data folder in your S3 bucket
TRANSFORM_DATA_PATH = "s3://cde-capstone/transform-data/"  # Folder to store transformed data

def download_parquet_from_s3(s3_key):
    """Downloads a Parquet file from S3."""
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=S3_REGION,
    )
    buffer = BytesIO()
    s3.download_fileobj(S3_BUCKET, s3_key, buffer)
    buffer.seek(0)
    return pd.read_parquet(buffer)

def upload_parquet_to_s3(df, s3_key):
    """Uploads a DataFrame as a Parquet file to S3."""
    buffer = BytesIO()
    df.to_parquet(buffer, engine="pyarrow", index=False)
    buffer.seek(0)
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=S3_REGION,
    )
    s3.upload_fileobj(buffer, S3_BUCKET, s3_key)
    print(f"Transformed file uploaded to S3: {S3_BUCKET}/{s3_key}")

def transform_data(df):
    """Transforms the raw data to select required attributes."""
    # Extract nested fields
    df["name_common"] = df["name"].apply(lambda x: x.get("common") if isinstance(x, dict) else None)
    df["name_official"] = df["name"].apply(lambda x: x.get("official") if isinstance(x, dict) else None)
    df["idd_root"] = df["idd"].apply(lambda x: x.get("root") if isinstance(x, dict) else None)
    df["idd_suffixes"] = df["idd"].apply(
    lambda x: x["suffixes"][0] if isinstance(x, dict) and "suffixes" in x and isinstance(x["suffixes"], list) and len(x["suffixes"]) > 0 else None
    )


    # Concatenate IDD root and suffix
    df["country_code"] = df.apply(
        lambda x: f"{x['idd_root']}{x['idd_suffixes']}" if x["idd_root"] and x["idd_suffixes"] else None,
        axis=1,
    )

    # Expand currencies and languages
    currencies = pd.json_normalize(df["currencies"], sep="_").iloc[:, 0]
    df["currency_code"] = currencies.apply(lambda x: list(x.keys())[0] if isinstance(x, dict) else None)
    df["currency_name"] = currencies.apply(lambda x: list(x.values())[0].get("name") if isinstance(x, dict) else None)
    df["currency_symbol"] = currencies.apply(lambda x: list(x.values())[0].get("symbol") if isinstance(x, dict) else None)

    # Drop unused columns
    required_columns = [
        "name_common", "name_official", "independent", "unMember",
        "startOfWeek", "country_code", "capital", "region",
        "subregion", "languages", "area", "population", "continents",
        "currency_code", "currency_name", "currency_symbol"
    ]
    df = df[required_columns]

    return df


def main():
    # List objects in the raw-data folder
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=S3_REGION,
    )
    raw_files = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix="raw-data/").get("Contents", [])

    if not raw_files:
        print("No files found in the raw-data folder.")
        return

    for file in raw_files:
        s3_key = file["Key"]
        if s3_key.endswith(".parquet"):
            print(f"Processing file: {s3_key}")

            # Download raw data
            raw_df = download_parquet_from_s3(s3_key)
            print(f"Downloaded raw data with shape: {raw_df.shape}")

            # Debug: Inspect the raw data schema
            print("Columns in raw data:")
            print(raw_df.columns)

            # Debug: Check nested fields
            print("Sample 'name' field:")
            print(raw_df["name"].head())

            print("Sample 'idd' field:")
            print(raw_df["idd"].head())

            # Transform data
            processed_df = transform_data(raw_df)
            print(f"Transformed data with shape: {processed_df.shape}")

            # Save transformed data to S3 under transform-data folder
            processed_file_name = s3_key.replace("raw-data/", "transform-data/")
            upload_parquet_to_s3(processed_df, processed_file_name)
            print(f"Uploaded transformed file to: {S3_BUCKET}/{processed_file_name}")

if __name__ == "__main__":
    main()
