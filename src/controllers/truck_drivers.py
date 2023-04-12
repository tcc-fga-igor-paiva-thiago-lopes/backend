import jwt
import requests
from flask_restful import Api
from sqlalchemy.exc import IntegrityError
from flask import request, current_app, Blueprint

from src.app import db
from src.models.truck_driver import TruckDriver
from src.controllers.common.item_api import ItemAPI
from src.controllers.common.group_api import GroupAPI
from src.controllers.common.utils import (
    simple_error_response,
    missing_required_fields,
    missing_required_fields_msg,
)

PERMITTED_PARAMS = ["name", "email", "password", "password_confirmation"]

controller = Blueprint(
    "truck_drivers_controller", __name__, url_prefix="/truck-drivers"
)

api = Api(controller)


@controller.errorhandler(IntegrityError)
def handle_integrity_error(_):
    return simple_error_response(
        "Email já cadastrado", requests.codes.unprocessable_entity
    )


resource_kwargs = {"model": TruckDriver, "permitted_params": PERMITTED_PARAMS}

api.add_resource(
    GroupAPI, "/", endpoint="truck_drivers", resource_class_kwargs=resource_kwargs
)
api.add_resource(
    ItemAPI, "/<int:id>", endpoint="truck_driver", resource_class_kwargs=resource_kwargs
)


@controller.route("/login", methods=["POST"])
def login():
    request_data = request.get_json(force=True)

    REQUIRED_FIELDS = [("email", "e-mail"), ("password", "senha")]

    missing_fields = missing_required_fields(request_data, REQUIRED_FIELDS)

    if len(missing_fields) > 0:
        return simple_error_response(
            missing_required_fields_msg(missing_fields),
            requests.codes.unprocessable_entity,
        )

    email = request_data.get("email")

    truck_driver = db.first_or_404(
        db.select(TruckDriver).filter_by(email=email),
        description=f"Usuário com e-mail {email} não encontrado",
    )

    if truck_driver.verify_password(request_data.get("password")):
        truck_driver.login()

        return {
            "token": jwt.encode(
                {"truck_driver_id": truck_driver.id, "ttl": -1},
                current_app.config["SECRET_KEY"],
                algorithm="HS256",
            ),
        }, requests.codes.ok

    return simple_error_response(
        "Usuário ou senha incorretos", requests.codes.unauthorized
    )
