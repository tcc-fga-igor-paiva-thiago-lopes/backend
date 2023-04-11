import requests
from flask_restful import Resource
from flask import request, make_response

from src.app import db
from src.controllers.common.utils import permitted_parameters


class ItemAPI(Resource):
    init_every_request = False

    def __init__(self, model, permitted_params, not_found_msg=None):
        self.model = model
        self.permitted_params = permitted_params
        self.not_found_msg = not_found_msg

    def _not_found_message(self):
        try:
            return self.not_found_msg or f"{self.model.FRIENDLY_NAME_SINGULAR} não encontrado"
        except AttributeError:
            return "Não encontrado"

    def _get_item(self, id):
        return db.get_or_404(self.model, id, description=self._not_found_message())

    def get(self, id):
        item = self._get_item(id)

        return make_response(item.to_json(), requests.codes.ok)

    def patch(self, id):
        item = self._get_item(id)

        request_data = request.get_json(force=True)

        item.update(**permitted_parameters(request_data, self.permitted_params))

        return make_response(item.to_json(), requests.codes.ok)

    def delete(self, id):
        item = self._get_item(id)

        item.destroy()

        return make_response("", requests.codes.no_content)
