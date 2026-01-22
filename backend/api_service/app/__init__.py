from flask import Flask
from flask_cors import CORS
from .config import config
from .routes.routes import bp
from app.logging_config import setup_logging
from app.error_handlers import register_error_handlers
from app.services.job_service import JobService

def create_app(config_object=config):
    setup_logging()
    app = Flask(__name__)
    app.config.from_object(config_object)

    CORS(app)

    app.extensions['job_service'] = JobService()

    app.register_blueprint(bp)
    register_error_handlers(app)
    return app