import requests
from flask import request, Blueprint
from sqlalchemy.exc import IntegrityError

from src.model.truck_driver import TruckDriver
from src.controllers.utils import simple_error_response

controller = Blueprint(
    "truck_driver_controller",
    __name__,
    url_prefix='/truck-drivers'
)


@controller.route('', methods=['GET'])
def list_truck_drivers():
    truck_drivers = TruckDriver.query.all()

    return list(map(lambda line: line.to_json(), truck_drivers))


@controller.route('/<int:truck_driver_id>', methods=['GET'])
def show_truck_driver(truck_driver_id):
    truck_driver = TruckDriver.query.get(truck_driver_id)

    if truck_driver is None:
        return simple_error_response(
            "Usuário não encontrado",
            requests.codes.not_found
        )

    return truck_driver.to_json()


@controller.route('', methods=['POST'])
def register_new_driver():
    request_data = request.get_json(force=True)

    REQUIRED_FIELDS = ["name", "email", "password", "password_confirmation"]

    missing_fields = []

    for field in REQUIRED_FIELDS:
        if request_data.get(field, None) is None:
            missing_fields.append(field)

    if len(missing_fields) > 0:
        return simple_error_response(
            f"Os seguintes campos são obrigatórios: {', '.join(missing_fields)}.",
            requests.codes.unprocessable_entity
        )

    try:
        truck_driver = TruckDriver(
            name=request_data.get("name"),
            email=request_data.get("email"),
            password=request_data.get("password"),
            password_confirmation=request_data.get("password_confirmation")
        )

        truck_driver.save()
    except IntegrityError:
        return simple_error_response(
            "Email já cadastrado",
            requests.codes.unprocessable_entity
        )
    except Exception as error:
        return simple_error_response(
            f"Falha ao salvar usuário: {error}",
            requests.codes.unprocessable_entity
        )

    return truck_driver.to_json(), requests.codes.created
