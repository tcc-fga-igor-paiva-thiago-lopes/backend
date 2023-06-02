from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE

from src.app import db

fields.Field.default_error_messages["required"] = "campo obrigatório não informado"

fields.Enum.default_error_messages[
    "unknown"
] = "Deve ser uma das seguintes opções: {choices}."

fields.Number.default_error_messages = {
    "invalid": "Não é um número válido",
    "too_large": "Número muito grande",
}

fields.DateTime.default_error_messages = {
    "invalid": "Não é uma data e hora válida",
}


class BaseSchema(SQLAlchemyAutoSchema):
    __abstract__ = True

    class Meta:
        sqla_session = db.session
        load_instance = True
        include_fk = True
        unknown = EXCLUDE

    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    def load(self, data, **kwargs):
        if isinstance(data, int):
            model = self.__class__.Meta.model

            return db.get_or_404(
                model,
                data,
                description=f"{model.FRIENDLY_NAME_SINGULAR} não encontrado",
            )

        return super().load(data, **kwargs)
