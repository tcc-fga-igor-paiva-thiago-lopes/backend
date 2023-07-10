from flask_restful import Api
from flask import Blueprint
from src.models.category import Category
from src.controllers.common.item_api import ItemAPI
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

group_resource_kwargs = {
    **resource_kwargs,
    "list_query": lambda user: user.categories,
    "user_association_fk": "truck_driver_id",
}

api.add_resource(
    GroupAPI,
    "/",
    endpoint="categories",
    resource_class_kwargs=group_resource_kwargs,
    methods=["POST", "GET", "PATCH", "DELETE"],
)

api.add_resource(
    ItemAPI,
    "/<int:id>",
    endpoint="category",
    resource_class_kwargs=resource_kwargs,
)
