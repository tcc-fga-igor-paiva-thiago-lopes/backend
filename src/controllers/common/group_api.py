import requests
from flask import request, jsonify
from flask.views import MethodView
from src.controllers.common.utils import permitted_parameters


class GroupAPI(MethodView):
    init_every_request = False

    def __init__(self, model, validator, permitted_params):
        self.model = model
        self.validator = validator
        self.permitted_params = permitted_params

    def get(self):
        items = self.model.query.all()

        return jsonify([item.to_json() for item in items])

    def post(self):
        request_data = request.get_json(force=True)

        # errors = self.validator.validate(request.json)

        # if errors:
        #     return jsonify(errors), 400

        item = self.model.create(
            **permitted_parameters(request_data, self.permitted_params)
        )

        return jsonify(item.to_json()), requests.codes.created
