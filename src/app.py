import requests
from flask import Flask, json
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import HTTPException

from src.controllers.common.utils import simple_error_response

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()


def create_app(is_testing=False):
    """
    Create the Flask app
    """
    app = Flask(__name__)

    if is_testing:
        app.config.from_object("src.config.TestConfig")
    else:
        app.config.from_object("src.config.Config")

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)

    @app.errorhandler(Exception)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        app.log_exception(e)
        if isinstance(e, HTTPException):
            response = e.get_response()
            response.data = json.dumps({"message": e.description})
            response.content_type = "application/json"

            return response

        return simple_error_response(
            "Erro interno do servidor", requests.codes.internal_server_error
        )

    from src.controllers.truck_drivers import controller as truck_drivers_controller

    app.register_blueprint(truck_drivers_controller)

    return app
