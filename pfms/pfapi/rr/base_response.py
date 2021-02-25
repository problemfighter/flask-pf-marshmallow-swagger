
from marshmallow import Schema, fields


class BaseResponse(Schema):
    status = fields.String()
    code = fields.String()


class MessageResponse(BaseResponse):
    message = fields.String()


class ErrorResponse(MessageResponse):
    error = fields.String()
