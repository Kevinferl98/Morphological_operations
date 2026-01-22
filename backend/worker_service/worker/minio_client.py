import boto3
from botocore.client import Config
from worker.config import config
import io

class MinioClient:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            endpoint_url=config.MINIO_ENDPOINT,
            aws_access_key_id=config.MINIO_ACCESS_KEY,
            aws_secret_access_key=config.MINIO_SECRET_KEY,
            config=Config(signature_version="s3v4")
        )

    def put_bytes(self, object_name: str, data: bytes, content_type="image/png") -> None:
        self.client.put_object(
            Bucket=config.MINIO_BUCKET,
            Key=object_name,
            Body=io.BytesIO(data),
            ContentType=content_type
        )

    def get_bytes(self, object_name: str) -> bytes:
        response = self.client.get_object(Bucket=config.MINIO_BUCKET, Key=object_name)
        return response['Body'].read()