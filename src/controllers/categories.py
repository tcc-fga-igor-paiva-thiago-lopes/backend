from flask_restful import Api
from flask import Blueprint
from src.models.category import Category
from src.controllers.common.group_api import GroupAPI
from src.schemas.category_schema import CategorySchema

PERMITTED_PARAMS = ["name", "color"]

controller = Blueprint("categories_controller", __name__, url_prefix="/categories")

api = Api(controller)

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
    methods=["POST", "GET", "DELETE"],
)
