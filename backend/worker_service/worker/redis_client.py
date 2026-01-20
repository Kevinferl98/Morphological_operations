import json
import os
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")


class RedisClient:
    def __init__(self):
        self.redis = redis.Redis.from_url(REDIS_URL)

    def get_job(self, job_id):
        data = self.redis.get(f"job:{job_id}")
        return json.loads(data) if data else None

    def update_job(self, job_id, payload):
        self.redis.set(f"job:{job_id}", json.dumps(payload))
