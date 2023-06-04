from flask import Blueprint
from flask_restful import Api
from marshmallow import ValidationError

from src.models.freight import Freight
from src.controllers.common.item_api import ItemAPI
from src.controllers.common.group_api import GroupAPI
from src.schemas.freight_schema import FreightSchema
from src.controllers.common.utils import (
    validation_error_response,
)

PERMITTED_PARAMS = [
    "name",
    "cargo",
    "status",
    "description",
    "contractor",
    "cargo_weight",
    "agreed_payment",
    "distance",
    "start_date",
    "due_date",
    "finished_date",
    "origin_city",
    "origin_state",
    "origin_country",
    "origin_latitude",
    "origin_longitude",
    "destination_city",
    "destination_state",
    "destination_country",
    "destination_latitude",
    "destination_longitude",
]

controller = Blueprint("freights_controller", __name__, url_prefix="/freights")

api = Api(controller)


@controller.errorhandler(ValidationError)
def handle_validation_error(error):
    return validation_error_response(error, "Falha ao validar frete")


resource_kwargs = {
    "model": Freight,
    "permitted_params": PERMITTED_PARAMS,
    "model_schema": FreightSchema,
}

group_resource_kwargs = {
    **resource_kwargs,
    "list_query": lambda user: user.freights,
    "user_association_fk": "truck_driver_id",
}

api.add_resource(
    GroupAPI,
    "/",
    endpoint="freights",
    resource_class_kwargs=group_resource_kwargs,
    methods=["GET", "POST"],
)

api.add_resource(
    ItemAPI,
    "/<int:id>",
    endpoint="freight",
    resource_class_kwargs=resource_kwargs,
)
