import typing
from marshmallow import fields, ValidationError


class ColorField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return bytes.hex(value)

    def _deserialize(self, value, attr, data, **kwargs):
        return self._validated(value)

    def _validated(self, value) -> bytes:
        if value is None:
            return None

        if value is True or value is False:
            raise self.make_error("invalid", input=value)
        try:
            return bytes.fromhex(value)
        except (TypeError, ValueError) as error:
            raise self.make_error("invalid", input=value) from error
