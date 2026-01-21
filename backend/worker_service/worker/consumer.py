import logging
import signal
import sys
from worker.rabbitmq_consumer import RabbitMQConsumer
from worker.redis_client import RedisClient
from worker.image_processor import process_job_logic
from worker.logging_config import setup_logging

logger = logging.getLogger(__name__)

def main():
    setup_logging()
    redis_client = RedisClient()

    def on_message_received(job_id):
        process_job_logic(job_id, redis_client)

    consumer = RabbitMQConsumer(callback=on_message_received)

    def stop_handler(sig, frame):
        logger.info("Shutdown signal received. Closing connections...")
        consumer.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, stop_handler)
    signal.signal(signal.SIGTERM, stop_handler)

    consumer.start()

if __name__ == "__main__":
    main()