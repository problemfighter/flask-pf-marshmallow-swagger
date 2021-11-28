from pfms.common.pfms_exception import PfMsException
from pfms.pfapi.base.pfms_base_schema import PfBaseSchema
from pfms.pfapi.pfms_cons import SUCCESS_CODE, ERROR_CODE, ERROR
from pfms.pfapi.rr.pfms_request_processor import PfRequestProcessor
from pfms.pfapi.rr.pfms_response_processor import PfResponseProcessor

request_processor = PfRequestProcessor()
response_processor = PfResponseProcessor()


class PfRequestResponse:

    def response(self):
        return response_processor

    def request(self):
        return request_processor

    def json_request_process(self, pf_schema: PfBaseSchema, existing_instance=None, is_validate_only: bool = False):
        return request_processor.validate_and_process(pf_schema, existing_instance, is_validate_only)

    def json_data_response(self, model, pf_schema: PfBaseSchema):
        return response_processor.data_response(model, pf_schema)

    def json_list_dic_data_response(self, data, many=False):
        return response_processor.list_dic_data_response(data, many)

    def json_validate_and_data_response(self, model, pf_schema: PfBaseSchema, message="Requested data is not available."):
        if not model:
            return response_processor.error(message)
        return response_processor.data_response(model, pf_schema)

    def check_empty_value_raise_exception(self, data, message="Empty value"):
        if not data:
            raise PfMsException(message_response=response_processor.error(message))
        return data

    def json_pagination_response(self, model_paginated, pf_schema: PfBaseSchema):
        return response_processor.paginated_data_response(model_paginated, pf_schema)

    def json_list_response(self, data, pf_schema: PfBaseSchema):
        return response_processor.data_list_response(data, pf_schema)

    def upload_request_preocess(self, pf_schema: PfBaseSchema, existing_instance=None):
        return request_processor.upload_request_validate(pf_schema, existing_instance)

    def success(self, message, code=SUCCESS_CODE, http_code=200):
        return response_processor.success(message, code, http_code=http_code)

    def error(self, message, code=ERROR_CODE, http_code=200):
        return response_processor.error(message, code, http_code=http_code)

    def error_response(self, errors: dict, message="Validation Error", status=ERROR, code=ERROR_CODE):
        return response_processor.error_response(errors=errors, message=message, status=status, code=code)

    def get_requested_data_value(self, key, default=None):
        return request_processor.get_requested_data_value(key, default)
