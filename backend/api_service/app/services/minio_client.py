import boto3
from botocore.client import Config
from app.config import config

class MinioClient:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            endpoint_url=config.MINIO_ENDPOINT,
            aws_access_key_id=config.MINIO_ACCESS_KEY,
            aws_secret_access_key=config.MINIO_SECRET_KEY,
            config=Config(signature_version="s3v4")
        )

    def generate_presigned_upload_url(self, image_key: str, expires_in=3600):
        return self.client.generate_presigned_url(
            "put_object",
            Params={"Bucket": config.MINIO_BUCKET, "Key": image_key},
            ExpiresIn=expires_in
        )
    
    def generate_presigned_download_url(self, image_key: str, expires_in=3600):
        return self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": config.MINIO_BUCKET, "Key": image_key},
            ExpiresIn=expires_in
        )
    
    def head_object(self, image_key: str):
        self.client.head_object(Bucket=config.MINIO_BUCKET, Key=image_key)