from marshmallow import fields, post_load, validate, validates_schema, ValidationError

from src.models.truck_driver import TruckDriver
from src.schemas.base_schema import BaseSchema


class TruckDriverSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = TruckDriver
        # Had to disable load_instance because it fails using password and password_confirmation
        load_instance = False
        exclude = ("password_digest",)

    last_sign_in_at = fields.DateTime(dump_only=True)
    email = fields.Email(
        required=True, error_messages={"invalid": "Não é um endereço de e-mail válido"}
    )

    password = fields.String(
        load_only=True,
        required=True,
        validate=validate.Length(
            min=8, error="Menor que o tamanho mínimo de {min} caracteres"
        ),
    )
    password_confirmation = fields.String(
        load_only=True,
        required=True,
        validate=validate.Length(
            min=8, error="Menor que o tamanho mínimo de {min} caracteres"
        ),
    )

    @post_load
    def make_truck_driver(self, data, **_):
        model = self.__class__.Meta.model

        return model(**data)

    @validates_schema(skip_on_field_errors=False)
    def validate_password_and_confirmation(self, data, **_):
        if data.get("password", None) != data.get("password_confirmation", None):
            raise ValidationError(
                {
                    "password": "Senha e confirmação devem ser iguais",
                    "password_confirmation": "Senha e confirmação devem ser iguais",
                }
            )


truck_driver_schema = TruckDriverSchema()
truck_drivers_schema = TruckDriverSchema(many=True)
