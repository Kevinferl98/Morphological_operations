from flask import Flask
from .config import DevelopmentConfig
from .extensions import executor
from .api.routes import bp
from app.logging_config import setup_logging

def create_app(config_object=DevelopmentConfig):
    setup_logging()
    app = Flask(__name__)
    app.config.from_object(config_object)

    executor.init_app(app)
    app.register_blueprint(bp)

    return app