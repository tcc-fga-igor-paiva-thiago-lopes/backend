from src.models.freight import Freight
from src.schemas.base_schema import BaseSchema


class FreightSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Freight


freight_schema = FreightSchema()
freights_schema = FreightSchema(many=True)
