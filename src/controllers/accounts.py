import requests
from flask import Blueprint
from flask_restful import Api
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from src.models.account import Account
from src.controllers.common.item_api import ItemAPI
from src.controllers.common.group_api import GroupAPI
from src.schemas.account_schema import AccountSchema
from src.controllers.common.utils import (
    validation_error_response,
    simple_error_response,
)

PERMITTED_PARAMS = [
    "identifier",
    "name",
    "value",
    "account_date",
    "description",
    "freight_identifier",
    "category_identifier",
]

controller = Blueprint("accounts_controller", __name__, url_prefix="/accounts")

api = Api(controller)


@controller.errorhandler(IntegrityError)
def handle_integrity_error(_):
    return simple_error_response(
        "O nome do gasto deve ser único por frete", requests.codes.unprocessable_entity
    )


@controller.errorhandler(ValidationError)
def handle_validation_error(error):
    return validation_error_response(error, "Falha ao validar conta")


resource_kwargs = {
    "model": Account,
    "permitted_params": PERMITTED_PARAMS,
    "model_schema": AccountSchema,
}

api.add_resource(
    GroupAPI,
    "/",
    endpoint="accounts",
    resource_class_kwargs=resource_kwargs,
    methods=["POST", "PATCH", "DELETE"],
)

api.add_resource(
    ItemAPI,
    "/<int:id>",
    endpoint="account",
    resource_class_kwargs=resource_kwargs,
)
