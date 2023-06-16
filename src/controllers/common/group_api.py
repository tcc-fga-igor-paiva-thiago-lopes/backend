import pytz
import requests
from datetime import datetime
from flask_restful import Resource
from flask import request, make_response
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required


from src.app import db
from src.controllers.common.utils import permitted_parameters, simple_error_response


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

    def _add_fields_to_import_data(self, data):
        params = permitted_parameters(data, self.permitted_params)

        if self.user_association_fk is not None:
            params[self.user_association_fk] = current_user.id

        params["synced_at"] = datetime.utcnow().replace(tzinfo=pytz.utc).isoformat()

        return params

    def _process_import_fields(self, import_data):
        return list(
            map(
                lambda freight_data: self._add_fields_to_import_data(freight_data),
                import_data,
            )
        )

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

    def patch(self):
        import_data = self._process_import_fields(request.get_json(force=True))

        # Using group_schema to validate fields
        self.group_schema.load(import_data, partial=True)

        if len(import_data) == 0:
            return simple_error_response(
                "Nenhum registro a sincronizar", requests.codes.bad_request
            )

        ret = self.model.upsert(data=import_data, unique_by=["identifier"])

        if len(import_data) == len(ret):
            return make_response(ret, requests.codes.ok)

        return make_response(ret, requests.codes.accepted)
