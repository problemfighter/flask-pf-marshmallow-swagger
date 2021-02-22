import types


class ActionsToSwagger:
    __ignore_verbs = {"HEAD", "OPTIONS"}

    def __init__(self, base_app, apispec):
        self.base_app = base_app
        self.apispec = apispec

    def __get_action_methods(self, rule):
        methods = []
        for method in rule.methods.difference(self.__ignore_verbs):
            methods.append(method)
        return methods

    def __get_path_param(self, rule):
        pass

    def __process_action_decorator(self, definition, rule):
        methods = self.__get_action_methods(rule)
        print(methods)

    def has_pfms_decorator(self, endpoint):
        try:
            pfms = endpoint.__pfms__
            if pfms == "PFMS":
                return True
        except:
            return False

    def __process_url(self):
        for rule in self.base_app.url_map.iter_rules():
            endpoint = self.base_app.view_functions[rule.endpoint]
            if isinstance(endpoint, types.FunctionType):
                function_name = endpoint.__name__
                if function_name and self.has_pfms_decorator(endpoint):
                    definition = endpoint(pfms_definition=True)
                    self.__process_action_decorator(definition, rule)

    def process(self):
        self.__process_url()
        return ""
