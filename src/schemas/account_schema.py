from src.schemas.base_schema import BaseSchema
from src.models.account import Account


class AccountSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Account


account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)
