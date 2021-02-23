import types

from pfms.swagger.pfms_definition import PFMSDefinition


class ActionsToSwagger:
    _ignore_verbs = {"HEAD", "OPTIONS"}
    _swagger_data_type = {"string": "string", "int": "integer", "float": "number", "path": "string", "any": "string",
                          "uuid": "string"}

    def __init__(self, base_app, apispec):
        self.base_app = base_app
        self.apispec = apispec

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

    def _process_action_decorator(self, definition: PFMSDefinition, rule):
        definition.methods = self._get_action_methods(rule)
        definition = self._get_path_param(definition, rule)
        print(definition)

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
