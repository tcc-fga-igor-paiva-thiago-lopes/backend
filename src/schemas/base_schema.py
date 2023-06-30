from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate, EXCLUDE

from src.app import db

fields.Field.default_error_messages["required"] = "campo obrigatório não informado"

fields.Enum.default_error_messages[
    "unknown"
] = "Deve ser uma das seguintes opções: {choices}."

fields.Number.default_error_messages.update(
    {
        "invalid": "Não é um número válido",
        "too_large": "Número muito grande",
    }
)

fields.DateTime.default_error_messages.update(
    {
        "invalid": "Não é uma data e hora válida",
    }
)

fields.String.default_error_messages.update(
    {"invalid": "Não é uma string (texto) válido"}
)

validate.Length.message_min = "Menor que o tamanho mínimo {min}"
validate.Length.message_max = "Maior que  o tamanho máximo {max}"
validate.Length.message_all = "Tamanho deve estar entre {min} e {max}"
validate.Length.message_equal = "Tamanho deve ser igual a {equal}"


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
