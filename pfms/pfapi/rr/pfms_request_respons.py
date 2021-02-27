from pfms.pfapi.base.pfms_base_schema import PfBaseSchema
from pfms.pfapi.rr.pfms_request_processor import PfRequestProcessor
from pfms.pfapi.rr.pfms_response_processor import PfResponseProcessor


class PfRequestResponse(PfRequestProcessor, PfResponseProcessor):

    def json_request_process(self, pf_schema: PfBaseSchema):
        return self.validate_and_process(pf_schema)

    def json_data_response(self, pf_schema: PfBaseSchema):
        return self.data_response(pf_schema)

    def json_pagination_response(self):
        pass

    def json_list_response(self):
        pass
