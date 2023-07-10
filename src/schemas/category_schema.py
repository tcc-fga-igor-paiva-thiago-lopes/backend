from marshmallow import post_load

from src.models.category import Category
from src.schemas.base_schema import BaseSchema
from src.schemas.data_types.color_field import ColorField


class CategorySchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Category

    color = ColorField(required=True)


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
