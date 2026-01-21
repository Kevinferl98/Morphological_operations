from flask import Flask
from flask_cors import CORS
from .config import DevelopmentConfig
from .routes.routes import bp
from app.logging_config import setup_logging
from app.error_handlers import register_error_handlers

def create_app(config_object=DevelopmentConfig):
    setup_logging()
    app = Flask(__name__)
    app.config.from_object(config_object)

    CORS(app)

    if not app.config.get("TESTING"):
        from app.services.job_service import JobService
        app.extensions['job_service'] = JobService()

    app.register_blueprint(bp)
    register_error_handlers(app)
    return app