from flask import Flask
from .config import DevelopmentConfig
from .extensions import executor
from .api.routes import bp

def create_app(config_object=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)

    executor.init_app(app)
    app.register_blueprint(bp)

    return app