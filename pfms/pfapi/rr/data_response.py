from marshmallow import fields
from pfms.pfapi.rr.base_response import BaseResponse


class DataResponse(BaseResponse):
    data = None

    def set_data(self, data, many=False):
        self.data = fields.Nested(data, many=many)
        return self
