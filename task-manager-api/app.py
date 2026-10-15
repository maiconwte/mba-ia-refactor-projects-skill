from datetime import datetime, timezone

from flask import Flask, jsonify
from flask_cors import CORS

import config.settings as settings
from database import db
from middlewares.error_handler import register_error_handlers
from routes.category_routes import category_bp
from routes.report_routes import report_bp
from routes.task_routes import task_bp
from routes.user_routes import user_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    CORS(app)
    db.init_app(app)
    register_error_handlers(app)

    app.register_blueprint(task_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(category_bp)

    @app.route("/health")
    def health():
        return {"status": "ok", "timestamp": str(datetime.now(timezone.utc))}

    @app.route("/")
    def index():
        return {"message": "Task Manager API", "version": "1.0"}

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
