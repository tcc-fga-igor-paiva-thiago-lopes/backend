import jwt
import requests
from flask import request, current_app, Blueprint
# from flask.views import MethodView
# from sqlalchemy.exc import IntegrityError

from src.model.truck_driver import TruckDriver
from src.controllers.common.utils import simple_error_response
from src.api import register_default_api

PERMITTED_PARAMS = ["name", "email", "password", "password_confirmation"]

controller = Blueprint(
    "truck_driver_controller",
    __name__,
    url_prefix="/truck-drivers"
)

register_default_api(
    app=controller,
    model=TruckDriver,
    name="truck-drivers",
    validator=None,
    permitted_params=PERMITTED_PARAMS
)


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
