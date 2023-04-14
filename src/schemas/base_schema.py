from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, EXCLUDE, pre_load

from src.app import db

fields.Field.default_error_messages["required"] = "campo obrigatório não informado"


class BaseSchema(SQLAlchemyAutoSchema):
    __abstract__ = True

    class Meta:
        sqla_session = db.session
        load_instance = True
        include_fk = True
        unknown = EXCLUDE

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @pre_load
    def filter_data(self, data, **_):
        return dict(filter(lambda pair: pair[0] != "id", data.items()))

    def load(self, data, **kwargs):
        if isinstance(data, int):
            model = self.__class__.Meta.model

            return db.get_or_404(
                model,
                data,
                description=f"{model.FRIENDLY_NAME_SINGULAR} não encontrado",
            )

        return super().load(data, **kwargs)
