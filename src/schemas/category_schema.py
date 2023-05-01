from marshmallow import fields, post_load

from src.models.category import Category
from src.schemas.base_schema import BaseSchema


class CategorySchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Category

    @post_load
    def make_categories(self, data, **_):
        model = self.__class__.Meta.model

        return model(**data)


category_schema = CategorySchema()
categorys_schema = CategorySchema(many=True)
