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

    app.config.from_object("src.config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    from src.controllers.truck_drivers import truck_driver_controller
    app.register_blueprint(truck_driver_controller)

    CORS(app, resources={r"/*": {"origins": "*"}})

    Api(app)  # api =

    # return app, api, db
    return app