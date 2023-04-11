import jwt
import requests
from flask_restful import Api
from sqlalchemy.exc import IntegrityError
from flask import request, current_app, Blueprint

from src.models.truck_driver import TruckDriver
from src.controllers.common.item_api import ItemAPI
from src.controllers.common.group_api import GroupAPI
from src.controllers.common.utils import simple_error_response

PERMITTED_PARAMS = ["name", "email", "password", "password_confirmation"]

controller = Blueprint(
    "truck_driver_controller",
    __name__,
    url_prefix="/truck-drivers"
)

api = Api(controller)


@controller.errorhandler(IntegrityError)
def handle_integrity_error(_):
    return simple_error_response(
        "Email já cadastrado",
        requests.codes.unprocessable_entity
    )


resource_kwargs = {"model": TruckDriver, "permitted_params": PERMITTED_PARAMS}

api.add_resource(GroupAPI, "/", endpoint="truck_drivers", resource_class_kwargs=resource_kwargs)
api.add_resource(ItemAPI, "/<int:id>", endpoint="truck_driver", resource_class_kwargs=resource_kwargs)


@controller.route("/login", methods=["POST"])
def login():
    request_data = request.get_json(force=True)

    REQUIRED_FIELDS = ["email", "password"]

    for field in REQUIRED_FIELDS:
        if request_data.get(field, None) is None:
            return simple_error_response(
                "Email e senha são obrigatórios",
                requests.codes.unprocessable_entity
            )

    email = request_data.get("email")

    truck_driver = TruckDriver.query.filter_by(email=email).first()

    if not truck_driver:
        return simple_error_response(
            f"Usuário com email {email} não encontrado",
            requests.codes.not_found
        )

    if (truck_driver.verify_password(request_data.get("password"))):

        truck_driver.login()

        return {
            "token": jwt.encode(
                {"truck_driver_id": truck_driver.id, "ttl": -1},
                current_app.config["SECRET_KEY"],
                algorithm="HS256"
            ),
        }, requests.codes.ok

    return simple_error_response(
        "Senha incorreta",
        requests.codes.unauthorized
    )
