from marshmallow import post_load

from src.models.category import Category
from src.schemas.base_schema import BaseSchema
from src.schemas.data_types.color_field import ColorField


class CategorySchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        load_instance = False
        model = Category

    color = ColorField(required=True)

    @post_load
    def make_categories(self, data, **_):
        model = self.__class__.Meta.model

        return model(**data)


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
