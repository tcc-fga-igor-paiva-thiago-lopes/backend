import requests
from flask_restful import Api
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    current_user,
)
from sqlalchemy.exc import IntegrityError
from flask import Blueprint
from marshmallow import ValidationError
from src.app import db, jwt
from src.models.category import Category
from src.controllers.common.group_api import GroupAPI
from src.controllers.common.utils import (
    simple_error_response,
    validation_error_response,
)
from src.schemas.category_schema import CategorySchema

PERMITTED_PARAMS = ["name", "email", "password", "password_confirmation"]

controller = Blueprint("categories_controller", __name__, url_prefix="/categories")

api = Api(controller)


@controller.errorhandler(IntegrityError)
def handle_integrity_error(_):
    return simple_error_response(
        "Email já cadastrado", requests.codes.unprocessable_entity
    )


@controller.errorhandler(ValidationError)
def handle_validation_error(error):
    return validation_error_response(error, "Falha ao validar usuário")


resource_kwargs = {
    "model": Category,
    "permitted_params": PERMITTED_PARAMS,
    "model_schema": CategorySchema,
}

api.add_resource(
    GroupAPI,
    "/",
    endpoint="categories",
    resource_class_kwargs=resource_kwargs,
    methods=["POST"],
)
