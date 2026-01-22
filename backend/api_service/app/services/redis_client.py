import json
import redis
from app.config import config

class RedisClient:
    def __init__(self):
        self.redis = redis.Redis.from_url(config.REDIS_URL)

    def get_job(self, job_id):
        data = self.redis.get(f"job:{job_id}")
        return json.loads(data) if data else None

    def update_job(self, job_id, payload):
        self.redis.set(f"job:{job_id}", json.dumps(payload))
