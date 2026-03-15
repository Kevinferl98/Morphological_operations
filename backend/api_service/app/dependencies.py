from fastapi import Depends
from app.services.redis_client import RedisClient
from app.services.minio_client import MinioClient
from app.services.rabbitmq_publisher import RabbitMQPublisher
from app.services.job_service import JobService

redis_client = RedisClient()
minio_client = MinioClient()
rabbitmq_publisher = RabbitMQPublisher()

def get_redis_client():
    return redis_client

def get_minio_client():
    return minio_client

def get_rabbitmq_publisher():
    return rabbitmq_publisher

def get_job_service(
    redis: RedisClient = Depends(get_redis_client),
    publisher: RabbitMQPublisher = Depends(get_rabbitmq_publisher),
    minio_client: MinioClient = Depends(get_minio_client)
):
    return JobService(redis, publisher, minio_client)