from marshmallow import fields, validate

from src.schemas.base_schema import BaseSchema
from src.models.freight import Freight, FreightCargoEnum, FreightStatusEnum


class FreightSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Freight

    cargo = fields.Enum(FreightCargoEnum, by_value=True)
    status = fields.Enum(FreightStatusEnum, by_value=True)

    origin_state = fields.String(
        required=True,
        validate=validate.Length(
            max=2, error="Maior que o tamanho máximo de 2 caracteres"
        ),
    )

    destination_state = fields.String(
        required=True,
        validate=validate.Length(
            max=2, error="Maior que o tamanho máximo de 2 caracteres"
        ),
    )


freight_schema = FreightSchema()
freights_schema = FreightSchema(many=True)
