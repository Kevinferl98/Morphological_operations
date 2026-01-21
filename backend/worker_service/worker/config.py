import os

class Config:
    ENV = os.getenv("APP_ENV", "development")
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t") or ENV == "development"
    TESTING = ENV == "testing"

    RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
    QUEUE_NAME = os.getenv("QUEUE_NAME", "image_jobs")
    
    REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
    
    LOG_LEVEL = "DEBUG" if DEBUG else os.getenv("LOG_LEVEL", "INFO")

config = Config()