import json
import logging
import os
import pika

logger = logging.getLogger(__name__)

RABBITMQ_URL = os.getenv(
    "RABBITMQ_URL",
    "amqp://guest:guest@rabbitmq:5672/"
)
QUEUE_NAME = "image_jobs"


class RabbitMQConsumer:
    def __init__(self, callback):
        self.callback = callback
        params = pika.URLParameters(RABBITMQ_URL)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=QUEUE_NAME, durable=True)

    def start(self):
        logger.info("Worker listening on queue %s", QUEUE_NAME)

        def on_message(ch, method, properties, body):
            try:
                payload = json.loads(body)
                self.callback(payload["job_id"])
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                logger.exception("Job failed")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message)
        self.channel.start_consuming()
