

class ActionsToSwagger():

    def __init__(self, base_app, apispec):
        self.base_app = base_app
        self.apispec = apispec

    def __process_url(self):
        ignore_verbs = {"HEAD", "OPTIONS"}
        for rule in self.base_app.url_map.iter_rules():
            endpoint = self.base_app.view_functions[rule.endpoint]
            # get_decorators(endpoint)
            for verb in rule.methods.difference(ignore_verbs):
                print(rule.rule + " " + verb)


    def process(self):
        self.__process_url()
        return ""