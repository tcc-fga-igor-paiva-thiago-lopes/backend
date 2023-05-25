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
        user_association=None,
        user_association_fk=None,
    ):
        self.model = model
        self.permitted_params = permitted_params
        self.item_schema = model_schema()
        self.group_schema = model_schema(many=True)
        self.user_association = user_association
        self.user_association_fk = user_association_fk

    def _get_records(self):
        if self.user_association is not None:
            return getattr(current_user, self.user_association)

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
