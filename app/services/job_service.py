import uuid
from app.services.image_processing_service import ImageProcessingService
import logging
import redis
import json
import os

logger = logging.getLogger(__name__)

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

class JobService:
    def __init__(self):
        self.redis = redis.Redis.from_url(REDIS_URL)
        self.image_service = ImageProcessingService()

    def create_job(self, file_bytes, form_data, executor, ttl_seconds=3600):
        job_id = str(uuid.uuid4())
        job_key = f"job:{job_id}"

        job_data = {
            "status": "pending",
            "result": None,
            "error": None
        }

        self.redis.set(job_key, json.dumps(job_data), ex=ttl_seconds)
        logger.info("Job %s created", job_id)

        executor.submit(self._run_job, job_key, file_bytes, form_data, ttl_seconds)
        return job_id

    def _run_job(self, job_key, file_bytes, form_data, ttl_seconds):
        try:
            logger.info("Job %s started", job_key)
            job_data = json.loads(self.redis.get(job_key))
            job_data["status"] = "running"
            self.redis.set(job_key, json.dumps(job_data), ex=ttl_seconds)

            result = self.image_service.process(file_bytes, form_data)

            job_data["status"] = "done"
            job_data["result"] = result
            self.redis.set(job_key, json.dumps(job_data), ex=ttl_seconds)
            logger.info("Job %s completed successfully", job_key)
        except Exception as e:
            logger.exception("Job %s failed", job_key)
            job_data["status"] = "error"
            job_data["error"] = str(e)
            self.redis.set(job_key, json.dumps(job_data), ex=ttl_seconds)

    def get_job(self, job_id):
        job_key = f"job:{job_id}"
        job_data = self.redis.get(job_key)
        if not job_data:
            return None
        return json.loads(job_data)