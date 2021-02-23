import types


class ActionsToSwagger:

    _ignore_verbs = {"HEAD", "OPTIONS"}
    _swagger_data_type = {"string": "string", "int": "integer", "float": "number", "path": "string", "any": "string", "uuid": "string"}

    def __init__(self, base_app, apispec):
        self.base_app = base_app
        self.apispec = apispec

    def _get_action_methods(self, rule):
        methods = []
        for method in rule.methods.difference(self._ignore_verbs):
            methods.append(method)
        return methods

    def  _extract_url_to_params(self, url):
        url_map = {}
        if url:
            fragments = url.split("/")
            for fragment in fragments:
                if fragment and fragment.startswith("<"):
                    type_input = fragment.replace("<", "").replace(">", "").split(":")
                    if len(type_input) == 2 and (type_input[0] in self._swagger_data_type):
                        url_map[type_input[1]] = self._swagger_data_type[type_input[0]]
                    else:
                        url_map[type_input[0]] = "string"
        return url_map

    def _get_path_param(self, rule):
        path = []
        data_type = self._extract_url_to_params(rule.rule)
        for param in rule.arguments:
            if param in data_type:
                path.append((param, data_type[param], True))
        return path

    def _process_action_decorator(self, definition, rule):
        methods = self._get_action_methods(rule)
        path_param = self._get_path_param(rule)
        print(methods)

    def _has_pfms_decorator(self, endpoint):
        try:
            pfms = endpoint.__pfms__
            if pfms == "PFMS":
                return True
        except:
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
