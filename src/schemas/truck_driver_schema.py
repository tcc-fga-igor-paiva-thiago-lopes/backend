from marshmallow import fields, post_load

from src.app import db
from src.models.truck_driver import TruckDriver
from src.schemas.base_schema import BaseSchema


class TruckDriverSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = TruckDriver
        load_instance = False
        exclude = ("password_digest",)
        additional = ("password", "password_confirmation")

    email = fields.Email(
        required=True, error_messages={"invalid": "Não é um endereço de e-mail válido"}
    )

    @post_load
    def make_truck_driver(self, data, **kwargs):
        model = self.__class__.Meta.model

        if kwargs.get("partial", None):
            return db.one_or_404(
                db.select(model).filter_by(**data),
                description=f"{model.FRIENDLY_NAME_SINGULAR} não encontrado",
            )

        return model(**data)


truck_driver_schema = TruckDriverSchema()
truck_drivers_schema = TruckDriverSchema(many=True)
