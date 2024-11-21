# variables.tf

variable "aws_region" {
  description = "The AWS region to deploy resources to"
  default     = "ap-south-1" 
}

variable "aws_access_key" {
  description = "AWS access key"
  type        = string
}

variable "aws_secret_key" {
  description = "AWS secret key"
  type        = string
}

variable "s3_bucket_name" {
  description = "The name of the S3 bucket for raw and processed data"
  default     = "cde-capstone"
}
