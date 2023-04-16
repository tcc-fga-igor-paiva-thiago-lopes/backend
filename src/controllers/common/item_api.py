import requests
from flask_restful import Resource
from flask import request, make_response

from src.controllers.common.utils import permitted_parameters


class ItemAPI(Resource):
    init_every_request = False

    def __init__(self, model, permitted_params, model_schema):
        self.model = model
        self.permitted_params = permitted_params
        self.item_schema = model_schema()

    def _get_item(self, id):
        return self.item_schema.load(id)

    def get(self, id):
        item = self._get_item(id)

        return make_response(self.item_schema.dump(item), requests.codes.ok)

    def patch(self, id):
        item = self._get_item(id)

        request_data = request.get_json(force=True)

        item.update(**permitted_parameters(request_data, self.permitted_params))

        return make_response(self.item_schema.dump(item), requests.codes.ok)

    def delete(self, id):
        item = self._get_item(id)

        item.destroy()

        return make_response("", requests.codes.no_content)
