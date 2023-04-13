import requests
from flask_restful import Resource
from flask import request, make_response

from src.app import db


class GroupAPI(Resource):
    init_every_request = False

    def __init__(self, model, permitted_params, model_schema):
        self.model = model
        self.permitted_params = permitted_params
        self.item_schema = model_schema()
        self.group_schema = model_schema(many=True)

    def get(self):
        items = db.session.execute(db.select(self.model)).scalars()

        return make_response(self.group_schema.dump(items), requests.codes.ok)

    def post(self):
        item = self.item_schema.load(request.get_json(force=True))
        item.save()

        return make_response(self.item_schema.dump(item), requests.codes.created)
