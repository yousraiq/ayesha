from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import sys
import logging

# Add the app directory to the Python path programmatically
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../dag')))

# Import your custom scripts
import extract  # Correct the import here
import transform

# Define your S3 bucket structure
S3_BUCKET = "cde-capstone"
RAW_FOLDER = "raw-data/"
PROCESSED_FOLDER = "transform-data/"

# Default args for the DAG
default_args = {
    "owner": "Ayesha",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define the DAG
with DAG(
    "capstone_etl",
    default_args=default_args,
    description="Extract and Transform Data Pipeline",
    schedule_interval="0 12 * * *",  # Daily at noon
    start_date=datetime(2024, 11, 1),
    catchup=False,
) as dag:

    # Task 1: Extract data from API to S3
    def extract_task():
        api_url = "https://restcountries.com/v3.1/all"
        logging.info("Starting data extraction...")
        try:
            extract.main(api_url, S3_BUCKET, RAW_FOLDER)  # Correct function call
            logging.info("Data extraction completed.")
        except Exception as e:
            logging.error(f"Extraction failed: {e}")
            raise

    extract_data = PythonOperator(
        task_id="extract_data",
        python_callable=extract_task,
    )

    # Task 2: Transform raw data from S3 and save to processed folder
    def transform_task():
        raw_file = f"{RAW_FOLDER}/latest_raw.parquet"
        processed_file = f"{PROCESSED_FOLDER}/latest_processed.parquet"
        logging.info("Starting data transformation...")
        try:
            # Download the raw data from S3
            raw_df = transform.download_parquet_from_s3(raw_file)  # Correct function
            transformed_df = transform.transform_data(raw_df)  # Correct function
            transform.upload_parquet_to_s3(transformed_df, processed_file)  # Correct function
            logging.info("Data transformation completed.")
        except Exception as e:
            logging.error(f"Transformation failed: {e}")
            raise

    transform_data = PythonOperator(
        task_id="transform_data",
        python_callable=transform_task,
    )

    # Task dependencies
    extract_data >> transform_data
