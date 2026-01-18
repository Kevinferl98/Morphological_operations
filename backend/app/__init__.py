from flask import Flask
from flask_cors import CORS
from .config import DevelopmentConfig
from .extensions import executor
from .api.routes import bp
from app.logging_config import setup_logging
from app.error_handlers import register_error_handlers

def create_app(config_object=DevelopmentConfig):
    setup_logging()
    app = Flask(__name__)
    app.config.from_object(config_object)

    CORS(app)

    executor.init_app(app)
    app.register_blueprint(bp)
    register_error_handlers(app)

    return app