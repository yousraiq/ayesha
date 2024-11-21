# main.tf

provider "aws" {
  region = "ap-south-1" 
  access_key = "AKIAU6VTTFBOJVZS6FWM"
  secret_key = "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"
}

resource "aws_s3_bucket" "cde_capstone_bucket" {
  bucket = "cde-capstone"
  acl    = "private"
}

resource "aws_s3_bucket_object" "raw_data" {
  bucket = aws_s3_bucket.cde_capstone_bucket.bucket
  key    = "raw-data/"
  acl    = "private"
}

resource "aws_s3_bucket_object" "transform_data" {
  bucket = aws_s3_bucket.cde_capstone_bucket.bucket
  key    = "transform-data/"
  acl    = "private"
}
