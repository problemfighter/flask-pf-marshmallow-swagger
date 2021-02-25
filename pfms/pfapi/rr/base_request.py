from marshmallow import Schema, fields
from marshmallow.base import SchemaABC


class BaseRequest(Schema):
    many: bool = False
    data = None

    def __init__(self, obj, many=False):
        self.data = fields.Nested(obj, many=many)
        super().__init__()
        self.many = many


