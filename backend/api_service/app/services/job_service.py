import uuid
import logging
import redis
import json
import os
import base64

from app.services.rabbitmq_publisher import RabbitMQPublisher

logger = logging.getLogger(__name__)

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

class JobService:
    def __init__(self, publisher=None, redis_client=None):
        self.redis = redis_client or redis.Redis.from_url(REDIS_URL)
        self.publisher = publisher or RabbitMQPublisher()

    def create_job(self, file_bytes, form_data, ttl_seconds=3600):
        job_id = str(uuid.uuid4())
        job_key = f"job:{job_id}"

        encoded_image = base64.b64encode(file_bytes).decode("utf-8")

        job_data = {
            "status": "pending",
            "image": encoded_image,
            "params": form_data,
            "result": None,
            "error": None
        }

        self.redis.set(job_key, json.dumps(job_data), ex=ttl_seconds)
        self.publisher.publish_job(job_id)

        logger.info("Job %s created", job_id)
        return job_id

    def get_job(self, job_id):
        job_key = f"job:{job_id}"
        job_data = self.redis.get(job_key)
        if not job_data:
            return None
        return json.loads(job_data)