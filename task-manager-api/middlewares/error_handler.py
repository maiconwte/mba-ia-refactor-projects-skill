from flask import jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return jsonify({"error": error.description or error.name}), error.code

    @app.errorhandler(Exception)
    def handle_unexpected(error):
        app.logger.exception("Unhandled error: %s", error)
        return jsonify({"error": "Erro interno do servidor"}), 500
