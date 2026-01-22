terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "6.28.0"
    }
  }
}

provider "aws" {
    region = "us-east-1"
    access_key = var.minio_access_key
    secret_key = var.minio_secret_key
    skip_credentials_validation = true
    skip_metadata_api_check = true
    skip_requesting_account_id = true
    s3_use_path_style = true
    endpoints {
        s3 = var.minio_endpoint
    }
}

resource "aws_s3_bucket" "images" {
    bucket = var.minio_bucket
}