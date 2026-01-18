import logging
import logging.config
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(name)s: %(message)s"
        },
        "detailed": {
            "format": (
                "[%(asctime)s] %(levelname)s "
                "[%(process)d:%(threadName)s] "
                "%(name)s: %(message)s"
            )
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default"
        }
    },

    "root": {
        "level": LOG_LEVEL,
        "handlers": ["console"]
    }
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)