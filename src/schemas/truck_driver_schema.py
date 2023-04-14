from marshmallow import fields, post_load

from src.models.truck_driver import TruckDriver
from src.schemas.base_schema import BaseSchema


class TruckDriverSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = TruckDriver
        # Had to disable load_instance because it fails using password and password_confirmation
        load_instance = False
        exclude = ("password_digest",)
        additional = ("password", "password_confirmation")

    email = fields.Email(
        required=True, error_messages={"invalid": "Não é um endereço de e-mail válido"}
    )

    @post_load
    def make_truck_driver(self, data, **_):
        model = self.__class__.Meta.model

        return model(**data)


truck_driver_schema = TruckDriverSchema()
truck_drivers_schema = TruckDriverSchema(many=True)
