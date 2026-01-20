import logging
from worker.rabbitmq_consumer import RabbitMQConsumer
from worker.redis_client import RedisClient
from worker.image_processor import process_image

logging.basicConfig(level=logging.INFO)

redis_client = RedisClient()

def handle_job(job_id):
    job = redis_client.get_job(job_id)
    if not job:
        raise RuntimeError("Job not found")

    try:
        result = process_image(job["image"], job["params"])
        job["status"] = "done"
        job["result"] = result
    except Exception as e:
        job["status"] = "error"
        job["error"] = str(e)

    redis_client.update_job(job_id, job)

if __name__ == "__main__":
    consumer = RabbitMQConsumer(handle_job)
    consumer.start()
