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
    migrate.init_app(app,db)

    from src.resources.truck_drivers import TruckDrivers

    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    api = Api(app)

    # FIXME: Create routes file
    api.add_resource(TruckDrivers, "/truck_driver")

    # return app, api, db
    return app

