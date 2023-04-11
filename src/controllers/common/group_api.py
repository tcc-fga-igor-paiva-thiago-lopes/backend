import requests
from flask_restful import Resource
from flask import request, make_response
from src.app import db
from src.controllers.common.utils import permitted_parameters


class GroupAPI(Resource):
    init_every_request = False

    def __init__(self, model, permitted_params):
        self.model = model
        self.permitted_params = permitted_params

    def get(self):
        items = db.session.execute(db.select(self.model)).scalars()

        return make_response([item.to_json() for item in items], requests.codes.ok)

    def post(self):
        request_data = request.get_json(force=True)

        item = self.model.create(
            **permitted_parameters(request_data, self.permitted_params)
        )

        return make_response(item.to_json(), requests.codes.created)
