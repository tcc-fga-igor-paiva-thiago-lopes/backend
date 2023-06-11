import requests
from flask_restful import Resource
from flask import request, make_response
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required


from src.app import db
from src.controllers.common.utils import permitted_parameters


class GroupAPI(Resource):
    init_every_request = False
    decorators = [jwt_required()]

    def __init__(
        self,
        model,
        permitted_params,
        model_schema,
        list_query=None,
        user_association_fk=None,
    ):
        self.model = model
        self.permitted_params = permitted_params
        self.item_schema = model_schema()
        self.group_schema = model_schema(many=True)
        self.list_query = list_query
        self.user_association_fk = user_association_fk

    def _get_records(self):
        if self.list_query is not None:
            return self.list_query(current_user)

        return db.session.execute(db.select(self.model)).scalars()

    def get(self):
        items = self._get_records()

        return make_response(self.group_schema.dump(items), requests.codes.ok)

    def post(self):
        request_data = request.get_json(force=True)

        params = permitted_parameters(request_data, self.permitted_params)

        if self.user_association_fk is not None:
            params[self.user_association_fk] = current_user.id

        item = self.item_schema.load(params)
        item.save()

        return make_response(self.item_schema.dump(item), requests.codes.created)
