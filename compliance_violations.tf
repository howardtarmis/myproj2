# INTENTIONAL IaC COMPLIANCE FIXTURE - do not deploy.
# Each resource demonstrates a common cloud security policy violation.

resource "aws_security_group" "wide_open" {
  name = "wide-open-demo"

  ingress {
    protocol    = "tcp"
    from_port   = 22
    to_port     = 22
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_ebs_volume" "unencrypted" {
  availability_zone = "us-east-1a"
  size              = 10
  encrypted         = false
}

resource "aws_s3_bucket" "public_data" {
  bucket = "public-compliance-fixture"
}

resource "aws_s3_bucket_public_access_block" "public_data" {
  bucket                  = aws_s3_bucket.public_data.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_iam_policy" "unrestricted" {
  name = "unrestricted-demo-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "*"
      Resource = "*"
    }]
  })
}
