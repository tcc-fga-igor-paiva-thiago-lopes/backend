from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE
from src.app import db

fields.Field.default_error_messages["required"] = "Campo obrigatório não informado"


class BaseSchema(SQLAlchemyAutoSchema):
    __abstract__ = True

    class Meta:
        sqla_session = db.session
        load_instance = True
        include_fk = True
        unknown = EXCLUDE
