from marshmallow import fields
from marshmallow.base import SchemaABC
from pfms.pfapi.rr.base_response import BaseResponse


class DataResponse(BaseResponse):
    _obj: SchemaABC = None

    def __init__(self, obj):
        super().__init__()
        self._obj = obj

    data = fields.Nested(_obj)
