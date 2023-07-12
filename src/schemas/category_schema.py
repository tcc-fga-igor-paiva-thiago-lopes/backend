from marshmallow import fields

from src.models.category import Category
from src.schemas.base_schema import BaseSchema


class CategorySchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Category

    color = fields.String(
        required=True,
        validate=lambda x: len(x) == 7
        and x[0] == "#"
        and all(c in "0123456789abcdef" for c in x[1:].lower()),
        error="Cor inválida",
    )


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
