from pfms.common.pfms_exception import PfMsException
from pfms.pfapi.base.pfms_base_schema import PfBaseSchema
from pfms.pfapi.rr.pfms_request_processor import PfRequestProcessor
from pfms.pfapi.rr.pfms_response_processor import PfResponseProcessor


class PfRequestResponse(PfRequestProcessor, PfResponseProcessor):

    def process(self, pf_schema: PfBaseSchema):
        json = self.get_json()
        raise PfMsException(message="Error")
        print("test")