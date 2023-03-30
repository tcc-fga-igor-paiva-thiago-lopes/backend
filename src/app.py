from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()


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

    from src.controllers.truck_drivers import controller as truck_driver_controller
    app.register_blueprint(truck_driver_controller)

    Api(app)

    return app
