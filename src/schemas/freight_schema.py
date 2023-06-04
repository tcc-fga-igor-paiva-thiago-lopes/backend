from marshmallow import fields

from src.schemas.base_schema import BaseSchema
from src.models.freight import Freight, FreightCargoEnum, FreightStatusEnum


class FreightSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Freight

    cargo = fields.Enum(FreightCargoEnum, by_value=True)
    status = fields.Enum(FreightStatusEnum, by_value=True)


freight_schema = FreightSchema()
freights_schema = FreightSchema(many=True)
