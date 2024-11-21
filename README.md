# CDE-CAPSTONE Project

## Overview
This project involves building a Data Platform for a travel agency that recommends tourist locations to customers. The platform processes data from the Country REST API and stores it in a Cloud Data Warehouse for predictive analytics. The solution includes:

- Extracting raw data from the Country API.
- Transforming the raw data into a structured format.
- Storing the transformed data in an S3 bucket in Parquet format.
- Orchestrating the entire process with Apache Airflow.
- Provisioning Infrastructure using Terraform.

## Project Components

### 1. Data Extraction
Data is extracted from the Country REST API and stored in the S3 Data Lake as Parquet files. The extracted data includes various attributes for each country, such as:

- Country Name
- Independence
- UN Member Status
- Currency Information
- Country Code (IDD)
- Capital, Region, Sub-Region
- Population, Area, and Continent

### 2. Data Transformation
The raw data from S3 is transformed by selecting the relevant attributes needed for the travel agency's predictive analytics. The transformation is done locally or in a database, and the transformed data is saved back to S3.

### 3. Orchestration with Apache Airflow
The Airflow DAG orchestrates the entire ETL process:

1. Extract the raw data from the API and store it in the `raw-data` folder on S3.
2. Transform the raw data as per the required attributes and store the result in the `transform-data` folder on S3.

### 4. Infrastructure Provisioning with Terraform
Terraform is used for the provisioning of the necessary infrastructure:

- IAM roles to allow access to S3.
- S3 buckets for storing raw and transformed data.
- Terraform State Management in cloud-based object storage for version control of the infrastructure.

### 5. CI/CD Pipeline
The project includes a basic CI/CD pipeline using GitHub for:

- Code linting to ensure best practices.
- Building and pushing Docker images for the extract and transform logic into a Cloud Container Registry.

## Project Setup and Installation

### Prerequisites:
- Python 3.x and Pip
- Terraform installed
- Docker installed
- AWS Account (for S3, IAM, etc.)

### 1. Clone the Repository
```bash
git clone https://github.com/yousraiq/ayesha.git

