from marshmallow import Schema, fields
from marshmallow.base import SchemaABC


class BaseRequest(Schema):
    _obj: SchemaABC = None
    many: bool = False

    def __init__(self, obj, many=False):
        super().__init__()
        self._obj = obj
        self.many = many

    data = fields.Nested(_obj, many=many)
