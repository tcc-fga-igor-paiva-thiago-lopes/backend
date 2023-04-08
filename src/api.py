from src.controllers.common.item_api import ItemAPI
from src.controllers.common.group_api import GroupAPI


def register_default_api(
    app,
    model,
    name,
    validator,
    permitted_params,
    group_methods=["GET", "POST"],
    item_methods=["GET", "POST", "PATCH", "DELETE"],
):
    register_group_api(
        app,
        model,
        name,
        validator,
        permitted_params,
        methods=group_methods
    )

    register_item_api(
        app,
        model,
        name,
        validator,
        permitted_params,
        methods=item_methods
    )


def register_item_api(
    app,
    model,
    name,
    validator,
    permitted_params,
    methods=["GET", "POST", "PATCH", "DELETE"]
):
    item_view = ItemAPI.as_view(f"{name}-item", model, validator, permitted_params)

    app.add_url_rule("/<int:id>", view_func=item_view, methods=methods)


def register_group_api(
    app,
    model,
    name,
    validator,
    permitted_params,
    methods=["GET", "POST"]
):
    group_view = GroupAPI.as_view(f"{name}-group", model, validator, permitted_params)

    app.add_url_rule("", view_func=group_view, methods=methods)
