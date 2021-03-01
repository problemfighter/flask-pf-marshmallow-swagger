from pfms.common.pfms_exception import PfMsException
from pfms.pfapi.base.pfms_base_schema import PfBaseSchema
from pfms.pfapi.rr.pfms_request_processor import PfRequestProcessor
from pfms.pfapi.rr.pfms_response_processor import PfResponseProcessor


class PfRequestResponse(PfRequestProcessor, PfResponseProcessor):

    def json_request_process(self, pf_schema: PfBaseSchema):
        return self.validate_and_process(pf_schema)

    def json_data_response(self, model, pf_schema: PfBaseSchema):
        return self.data_response(model, pf_schema)

    def json_validate_and_data_response(self, model, pf_schema: PfBaseSchema, message="Requested data is not available."):
        if not model:
            return self.error(message)
        return self.data_response(model, pf_schema)

    def check_empty_value_raise_exception(self, data, message="Empty value"):
        if not data:
            raise PfMsException(message_response=self.error(message))
        return data

    def json_pagination_response(self):
        pass

    def json_list_response(self):
        pass
