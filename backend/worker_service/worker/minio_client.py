from minio import Minio
from worker.config import config
import io

class MinioClient:
    def __init__(self):
        self.client = Minio(
            config.MINIO_ENDPOINT,
            access_key=config.MINIO_ACCESS_KEY,
            secret_key=config.MINIO_SECRET_KEY,
            secure=False
        )

        if not self.client.bucket_exists(config.MINIO_BUCKET):
            self.client.make_bucket(config.MINIO_BUCKET)

    def put_bytes(self, object_name: str, data: bytes, content_type="image/png") -> None:
        self.client.put_object(
            config.MINIO_BUCKET,
            object_name,
            data=io.BytesIO(data),
            length=len(data),
            content_type=content_type
        )

    def get_bytes(self, object_name: str) -> bytes:
        response = self.client.get_object(config.MINIO_BUCKET, object_name)
        return response.read()