import requests
from flask import request, make_response
from flask_restful import Resource
from src.controllers.common.utils import permitted_parameters


class GroupAPI(Resource):
    init_every_request = False

    def __init__(self, model, validator, permitted_params):
        self.model = model
        self.validator = validator
        self.permitted_params = permitted_params

    def get(self):
        items = self.model.query.all()

        return make_response([item.to_json() for item in items], requests.codes.ok)

    def post(self):
        request_data = request.get_json(force=True)

        # errors = self.validator.validate(request.json)

        # if errors:
        #     return jsonify(errors), 400

        item = self.model.create(
            **permitted_parameters(request_data, self.permitted_params)
        )

        return make_response(item.to_json(), requests.codes.created)
