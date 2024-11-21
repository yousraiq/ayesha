# outputs.tf

output "s3_bucket_name" {
  description = "The name of the S3 bucket"
  value       = aws_s3_bucket.cde_capstone_bucket.bucket
}

output "raw_data_path" {
  description = "The path to the raw data folder in the S3 bucket"
  value       = "${aws_s3_bucket.cde_capstone_bucket.bucket}/raw-data/"
}

output "transform_data_path" {
  description = "The path to the transform data folder in the S3 bucket"
  value       = "${aws_s3_bucket.cde_capstone_bucket.bucket}/transform-data/"
}
