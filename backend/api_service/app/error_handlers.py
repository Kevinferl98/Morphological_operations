import logging
from flask import jsonify
from app.exceptions import AppError

logger = logging.getLogger(__name__)

def register_error_handlers(app):

    @app.errorhandler(AppError)
    def handle_app_error(error):
        logger.warning("Handled app error: %s", error)
        return jsonify({
            "error": error.message
        }), error.status_code
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        logger.exception("Unhandled exception")
        return jsonify({
            "error": "Internal server error"
        }), 500