import requests
from flask_restful import Api
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    current_user,
)
from sqlalchemy.exc import IntegrityError
from flask import request, Blueprint
from marshmallow import ValidationError
from src.app import db, jwt
from src.models.truck_driver import TruckDriver
from src.controllers.common.group_api import GroupAPI
from src.controllers.common.utils import (
    required_fields,
    simple_error_response,
    fields_errors_response,
    validation_error_response,
)
from src.schemas.truck_driver_schema import TruckDriverSchema

PERMITTED_PARAMS = ["name", "email", "password", "password_confirmation"]

controller = Blueprint(
    "truck_drivers_controller", __name__, url_prefix="/truck-drivers"
)

api = Api(controller)


@controller.errorhandler(IntegrityError)
def handle_integrity_error(_):
    return fields_errors_response(
        {"email": ["Email já cadastrado"]},
        "Email já cadastrado",
        requests.codes.unprocessable_entity,
    )


@controller.errorhandler(ValidationError)
def handle_validation_error(error):
    return validation_error_response(error, "Falha ao validar usuário")


resource_kwargs = {
    "model": TruckDriver,
    "permitted_params": PERMITTED_PARAMS,
    "model_schema": TruckDriverSchema,
}

api.add_resource(
    GroupAPI,
    "/",
    endpoint="truck_drivers",
    resource_class_kwargs=resource_kwargs,
    methods=["POST"],
)


@controller.route("/login", methods=["POST"])
@required_fields([("email", "e-mail"), ("password", "senha")])
def login():
    email = request.json.get("email")

    truck_driver = db.first_or_404(
        db.select(TruckDriver).filter_by(email=email),
        description=f"Usuário com e-mail {email} não encontrado",
    )

    if truck_driver.verify_password(request.json.get("password")):
        truck_driver.login()

        return {
            "name": truck_driver.name,
            "token": create_access_token(identity=truck_driver.id),
        }, requests.codes.ok

    return simple_error_response(
        "Usuário ou senha incorretos", requests.codes.unauthorized
    )


@controller.route("/authenticated", methods=["GET"])
@jwt_required()
def is_authenticated():
    return {"id": current_user.id}, requests.codes.ok


@controller.route("/who-am-i", methods=["GET"])
@jwt_required()
def who_am_i():
    return {"id": current_user.id, "email": current_user.email}, requests.codes.ok


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return db.get_or_404(TruckDriver, identity)
