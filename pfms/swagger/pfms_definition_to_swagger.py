from apispec import APISpec
from pfms.common.pfms_data_type import string
from pfms.pfapi.rr.api_request import single_request, bulk_request
from pfms.pfapi.rr.api_response import data_response
from pfms.pfapi.rr.base_response import MessageResponse, ErrorResponse
from pfms.swagger.pfms_definition import PFMSDefinition
from pfms.common.pfms_util import get_random_string
from pfms.swagger.pfms_swagger_schemas import get_parameter, IN_QUERY, IN_PATH, get_request_body


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

    def _is_bulk_request(self, content_type: str):
        if content_type.startswith("BULK"):
            return True
        return False

    def _is_list_response(self, content_type: str):
        if content_type.endswith("LIST"):
            return True
        return False

    def add_request_response_schema(self, definition: PFMSDefinition):
        if definition.request_body:
            if self._is_bulk_request(definition.request_type):
                req = bulk_request(definition.request_body)
            else:
                req = single_request(definition.request_body)
            self.add_component_schema(definition.request_component, req)

        if definition.response_obj:
            res = data_response(definition.response_obj)
            self.add_component_schema(definition.response_component, res)

    def get_tuple_value(self, data: tuple, index: int, default=None):
        try:
            return data[index]
        except:
            return default

    def _process_parameters(self, params, parameters, place):
        if params:
            for query in params:
                if isinstance(query, tuple) and len(query) != 0:
                    name = self.get_tuple_value(query, 0)
                    data_type = self.get_tuple_value(query, 1, string)
                    is_required = self.get_tuple_value(query, 2, False)
                    parameters.append(get_parameter(place, name, data_type, is_required))
        return parameters

    def get_parameters(self, definition: PFMSDefinition):
        parameters = []
        self._process_parameters(definition.query_param, parameters, IN_QUERY)
        self._process_parameters(definition.path_params, parameters, IN_PATH)

        if len(parameters) != 0:
            return parameters
        return None

    def get_request_body(self, definition: PFMSDefinition):
        if definition.request_body:
            return get_request_body(definition, self._is_bulk_request(definition.request_type))
        return None

    def get_responses(self, definition: PFMSDefinition):
        if definition.response_obj:
            print("--")
        return None

    def get_operations(self, definition: PFMSDefinition):
        operations = {}
        for method in definition.methods:
            request_body = self.get_request_body(definition)
            responses = self.get_responses(definition)
            method = method.lower()
            operations[method] = {}
            if request_body:
                operations[method]["requestBody"] = request_body
            if responses:
                operations[method]["responses"] = responses
        if len(operations):
            return operations
        return None

    def assemble(self, definition: PFMSDefinition):
        self.specification.path(
            path=definition.url,
            parameters=self.get_parameters(definition),
            operations=self.get_operations(definition)
        )

    def process(self, definition: PFMSDefinition):
        self.pre_process_definition(definition)
        self.add_request_response_schema(definition)
        print("xyz")
        self.assemble(definition)
