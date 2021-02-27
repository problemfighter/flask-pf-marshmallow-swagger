import json

from marshmallow import Schema, fields


class BaseResponse(Schema):
    status = fields.String()
    code = fields.String()

    def get_response_def(self, data: dict = None):
        if not data:
            data = {}
        data["status"] = fields.String()
        data["code"] = fields.String()
        return Schema.from_dict(data)

    def json(self, many=False) -> str:
        return self.dumps(self, many=many)



class MessageResponse(BaseResponse):
    message = fields.String()


class ErrorResponse(MessageResponse):
    error = fields.Dict(keys=fields.String(), values=fields.String())

