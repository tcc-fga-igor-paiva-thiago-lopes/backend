import requests
from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from src.model.truck_driver import TruckDriver
from src.controllers.utils import simple_error_response

from flask import Blueprint

truck_driver_controller = Blueprint(
    "truck_driver_controller",
    __name__,
    url_prefix='/truck-drivers'
)

@truck_driver_controller.route('/', methods=['GET'])
def list_truck_drivers():
    truck_drivers = TruckDriver.query.all()

    return list(map(lambda line: line.to_json(), truck_drivers))

@truck_driver_controller.route('/', methods=['POST'])
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

# class TruckDrivers(Resource):
#     def get(self):
#         truck_drivers = TruckDriver.query.all()

#         return list(map(lambda line: line.to_json(), truck_drivers))


#     def post(self):
#         request_data = request.get_json(force=True)
        
#         REQUIRED_FIELDS = ["name", "email", "password", "password_confirmation"]

#         missing_fields = []

#         for field in REQUIRED_FIELDS:
#             if request_data.get(field, None) is None:
#                 missing_fields.append(field)

#         if len(missing_fields) > 0:
#             return simple_error_response(
#                 f"Os seguintes campos são obrigatórios: {', '.join(missing_fields)}.",
#                 requests.codes.unprocessable_entity
#             )

#         try:
#             truck_driver = TruckDriver(
#                 name=request_data.get("name"),
#                 email=request_data.get("email"),
#                 password=request_data.get("password"),
#                 password_confirmation=request_data.get("password_confirmation")
#             )

#             truck_driver.save()
#         except IntegrityError:
#             return simple_error_response(
#                 "Email já cadastrado",
#                 requests.codes.unprocessable_entity
#             )        
#         except Exception as error:
#             return simple_error_response(
#                 f"Falha ao salvar usuário: {error}",
#                 requests.codes.unprocessable_entity
#             )

#         return truck_driver.to_json(), requests.codes.created
