from flask import Flask
from flask_cors import CORS

from src.config import settings
from src.middlewares.error_handler import register_error_handlers
from src.models.database import get_db
from src.views.routes import register_routes


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["DEBUG"] = settings.DEBUG
    CORS(app)
    register_routes(app)
    register_error_handlers(app)
    get_db()
    return app


app = create_app()


if __name__ == "__main__":
    print("=" * 50)
    print("SERVIDOR INICIADO")
    print("Rodando em http://localhost:5000")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=app.config["DEBUG"])
