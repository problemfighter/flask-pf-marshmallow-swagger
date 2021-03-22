from pfms.common.pfms_exception import PfMsException
from pfms.pfapi.base.pfms_base_schema import PfBaseSchema
from pfms.pfapi.rr.pfms_request_processor import PfRequestProcessor
from pfms.pfapi.rr.pfms_response_processor import PfResponseProcessor

request_processor = PfRequestProcessor()
response_processor = PfResponseProcessor()


class PfRequestResponse:

    def response(self):
        return response_processor

    def request(self):
        return request_processor

    def json_request_process(self, pf_schema: PfBaseSchema, existing_instance=None):
        return request_processor.validate_and_process(pf_schema, existing_instance)

    def json_data_response(self, model, pf_schema: PfBaseSchema):
        return response_processor.data_response(model, pf_schema)

    def json_list_dic_data_response(self, data):
        return response_processor.list_dic_data_response(data)

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

    def json_list_response(self):
        pass

    def upload_request_preocess(self, pf_schema: PfBaseSchema, existing_instance=None):
        return request_processor.upload_request_validate(pf_schema, existing_instance)
