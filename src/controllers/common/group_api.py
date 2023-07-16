import pytz
import requests
from datetime import datetime
from flask_restful import Resource
from flask import request, make_response
from flask_jwt_extended import current_user, jwt_required

from src.app import db
from src.models.models import table_to_model
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

    def _get_fk_table_from_column(self, col):
        foreign_keys = list(col.foreign_keys)

        if len(foreign_keys) == 0:
            return None

        return foreign_keys[0].target_fullname.split(".")[0]

    def _get_tables_identifiers_map(self):
        tables_identifier_to_id = {}

        fk_tables = map(
            self._get_fk_table_from_column,
            filter(
                lambda col: "truck_driver" not in col.name
                and len(col.foreign_keys) > 0,
                self.model.__table__.columns,
            ),
        )

        for fk_table in fk_tables:
            model = table_to_model[fk_table]

            tables_identifier_to_id[fk_table] = model.identifier_to_id(current_user)

        return tables_identifier_to_id

    def _add_fields_to_import_data(self, data, identifier_to_id):
        params = permitted_parameters(data, self.permitted_params)

        for key, value in params.items():
            if "_identifier" in key:
                fk_field = key.replace("_identifier", "_id")
                fk_table = fk_field.split("_")[0].upper()

                del params[key]
                params[fk_field] = identifier_to_id.get(fk_table).get(value, None)

        if self.user_association_fk is not None:
            params[self.user_association_fk] = current_user.id

        params["synced_at"] = datetime.utcnow().replace(tzinfo=pytz.utc).isoformat()

        return params

    def _process_import_fields(self, import_data):
        return list(
            map(
                lambda freight_data: self._add_fields_to_import_data(
                    freight_data, self._get_tables_identifiers_map()
                ),
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

        upserted_identifiers = self.model.upsert(
            data=import_data, unique_by=["identifier"]
        )

        if len(upserted_identifiers) == 0:
            return simple_error_response(
                "Não foi possível remover nenhum registro", requests.codes.bad_request
            )

        if len(import_data) == len(upserted_identifiers):
            return make_response(upserted_identifiers, requests.codes.ok)

        return make_response(upserted_identifiers, requests.codes.ok)

    def delete(self):
        identifiers = request.args.getlist("identifiers")

        if len(identifiers) == 0:
            return simple_error_response(
                "Nenhum registro a remover", requests.codes.bad_request
            )

        deleted_identifiers = self.model.destroy_by_identifiers(
            identifiers, current_user
        )

        if len(identifiers) == len(deleted_identifiers):
            return make_response(
                {"deleted": deleted_identifiers, "not_exists": []}, requests.codes.ok
            )

        error_identifiers = set(identifiers) - set(deleted_identifiers)

        existing_identifiers = set(
            db.session.execute(
                db.select(self.model.identifier).where(
                    self.model.truck_driver == current_user,
                    self.model.identifier.in_(error_identifiers),
                )
            ).scalars()
        )

        not_existing_identifiers = list(error_identifiers - existing_identifiers)

        return make_response(
            {"deleted": deleted_identifiers, "not_exists": not_existing_identifiers},
            requests.codes.ok,
        )
