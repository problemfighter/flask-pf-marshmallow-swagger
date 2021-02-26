import types

from apispec import APISpec
from pfms.swagger.pfms_definition import PFMSDefinition
from pfms.swagger.pfms_definition_to_swagger import PFMSDefinitionToSwagger


class ActionsToSwagger:
    _specification: APISpec
    _definition_to_swagger: PFMSDefinitionToSwagger
    _ignore_verbs = {"HEAD", "OPTIONS"}
    _swagger_data_type = {"string": "string", "int": "integer", "float": "number", "path": "string", "any": "string",
                          "uuid": "string"}

    def __init__(self, base_app, apispec: APISpec):
        self.base_app = base_app
        self._specification = apispec
        self._definition_to_swagger = PFMSDefinitionToSwagger(apispec)
        self._definition_to_swagger.init_default_things()

    def _get_action_methods(self, rule):
        methods = []
        for method in rule.methods.difference(self._ignore_verbs):
            methods.append(method)
        return methods

    def _extract_url_to_params(self, url):
        url_map = {}
        if url:
            fragments = url.split("/")
            for fragment in fragments:
                if fragment and fragment.startswith("<"):
                    actual_fragment = fragment
                    type_input = fragment.replace("<", "").replace(">", "").split(":")
                    if len(type_input) == 2 and (type_input[0] in self._swagger_data_type):
                        param_name = type_input[1]
                        url_map[param_name] = self._swagger_data_type[type_input[0]]
                    else:
                        url_map[type_input[0]] = "string"
                        param_name = type_input[0]
                    url = url.replace(actual_fragment, "{" + param_name + "}")
        return {"url": url, "url_map": url_map}

    def _get_path_param(self, definition: PFMSDefinition, rule) -> PFMSDefinition:
        path = []
        url_and_data_type = self._extract_url_to_params(rule.rule)
        data_type = url_and_data_type['url_map']
        for param in rule.arguments:
            if param in data_type:
                path.append((param, data_type[param], True))
        definition.url = url_and_data_type['url']
        definition.path_params = path
        return definition

    def _get_default_tag_name(self, definition: PFMSDefinition, rule):
        endpoint_name = rule.endpoint
        end = endpoint_name.find(".")
        total = len(endpoint_name)
        definition.tags = []
        if end != -1 and total > end:
            endpoint_name = endpoint_name[0:end]
            endpoint_name = endpoint_name.replace("_", " ")
            endpoint_name = endpoint_name.title()
            definition.tags.append(endpoint_name)
        else:
            definition.tags.append("Common")


    def _process_action_decorator(self, definition: PFMSDefinition, rule):
        definition = self._get_path_param(definition, rule)
        definition.methods = self._get_action_methods(rule)
        self._get_default_tag_name(definition, rule)
        self._definition_to_swagger.process(definition)

    def _has_pfms_decorator(self, endpoint) -> bool:
        try:
            pfms = endpoint.__pfms__
            if pfms == "PFMS":
                return True
        except:
            return False
        return False

    def _process_url(self):
        for rule in self.base_app.url_map.iter_rules():
            endpoint = self.base_app.view_functions[rule.endpoint]
            if isinstance(endpoint, types.FunctionType):
                function_name = endpoint.__name__
                if function_name and self._has_pfms_decorator(endpoint):
                    definition = endpoint(pfms_definition=True)
                    self._process_action_decorator(definition, rule)

    def process(self):
        self._process_url()
        return ""
