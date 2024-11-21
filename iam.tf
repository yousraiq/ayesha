# iam.tf

# provider "aws" {
#   region = "ap-south-1"  
# }

resource "aws_iam_policy" "s3_full_access" {
  name        = "S3FullAccess"
  description = "Grant full access to S3 bucket"
  policy      = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "s3:*"
        Resource = "arn:aws:s3:::cde-capstone/*"  
      }
    ]
  })
}

resource "aws_iam_role" "airflow_role" {
  name               = "airflow-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
        Effect    = "Allow"
        Sid       = ""
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "s3_full_access_attachment" {
  role       = aws_iam_role.airflow_role.name
  policy_arn = aws_iam_policy.s3_full_access.arn
}
