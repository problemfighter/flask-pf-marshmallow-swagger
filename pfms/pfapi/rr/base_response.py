
from marshmallow import Schema, fields


class BaseResponse(Schema):
    status = fields.String()
    code = fields.String()
