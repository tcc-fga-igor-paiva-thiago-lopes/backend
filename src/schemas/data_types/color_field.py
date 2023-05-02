import typing
from marshmallow import fields, ValidationError


class ColorField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return bytes.hex(value)

    def _deserialize(self, value, attr, data, **kwargs):
        return bytes.fromhex(value)
