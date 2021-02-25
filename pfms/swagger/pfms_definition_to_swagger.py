from apispec import APISpec
from pfms.pfapi.rr.api_request import single_request
from pfms.pfapi.rr.base_response import MessageResponse, ErrorResponse
from pfms.swagger.pfms_definition import PFMSDefinition
from pfms.common.pfms_util import get_random_string


class PFMSDefinitionToSwagger:

    specification: APISpec
    MESSAGE_RESPONSE: str = "MessageResponse"
    ERROR_DETAILS_RESPONSE: str = "ErrorDetailsResponse"

    def __init__(self, specification: APISpec):
        self.specification = specification

    def add_component_schema(self, key: str, data):
        if key not in self.specification.components.schemas:
            self.specification.components.schema(key, schema=data)

    def init_default_things(self):
        self.add_component_schema(self.MESSAGE_RESPONSE, MessageResponse)
        self.add_component_schema(self.ERROR_DETAILS_RESPONSE, ErrorResponse)

    def pre_process_definition(self, definition: PFMSDefinition):
        component_code = get_random_string(13).upper()
        definition.request_component = "Req" + component_code
        definition.response_component = "Res" + component_code

    def add_request_response_schema(self, definition: PFMSDefinition):
        if definition.request_body:
            req = single_request(definition.request_body)
            self.add_component_schema(definition.request_component, req)

        if definition.response_obj:
            self.add_component_schema(definition.response_component, definition.response_obj)

    def process(self, definition: PFMSDefinition):
        self.pre_process_definition(definition)
        self.add_request_response_schema(definition)
        print("xyz")
