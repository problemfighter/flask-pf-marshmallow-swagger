from marshmallow import Schema, fields
from pfms.pfapi.base.pfms_base_schema import PfBaseSchema


class BaseResponse(Schema):
    status = fields.String()
    code = fields.String()

    def get_data_response_def(self, data: dict = None):
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


class DataResponse(BaseResponse):
    data = None

    def get_list_data_type(self, data_list: list):
        if len(data_list) != 0:
            first_element = data_list[0]
            if isinstance(first_element, int):
                return fields.Integer
            if isinstance(first_element, dict):
                return fields.Dict
            if isinstance(first_element, float):
                return fields.Float
        return fields.String

    def add_data(self, data, many):
        field = None
        if isinstance(data, str):
            field = fields.String(default=data)
        if isinstance(data, dict):
            field = fields.Dict(default=data)
        elif isinstance(data, PfBaseSchema):
            field = fields.Nested(data, many=many)
        elif isinstance(data, list):
            field = fields.List(default=data, cls_or_instance=self.get_list_data_type(data))
        if field:
            self.data = data
            self.fields['data'] = field
            self.dump_fields['data'] = field
            self.declared_fields['data'] = field
            self.load_fields['data'] = field
