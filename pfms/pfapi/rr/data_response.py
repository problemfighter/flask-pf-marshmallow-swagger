from marshmallow import fields
from pfms.pfapi.rr.base_response import BaseResponse


class DataResponse(BaseResponse):
    obj = None

    def __init__(self, obj):
        self.obj = obj

    data = fields.Nested(obj)
