from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE
from src.app import db

fields.Field.default_error_messages["required"] = "campo obrigatório não informado"


class BaseSchema(SQLAlchemyAutoSchema):
    __abstract__ = True

    class Meta:
        sqla_session = db.session
        load_instance = True
        include_fk = True
        unknown = EXCLUDE

    def load(self, data, **kwargs):
        if isinstance(data, int):
            kwargs["partial"] = True

            return super().load({"id": data}, **kwargs)

        if data.get("id", None) is not None:
            kwargs["partial"] = True

            return super().load({"id": data["id"]}, **kwargs)

        return super().load(data, **kwargs)
