
class PFMarshmallowSwagger:

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('SQLITE3_DATABASE', ':memory:')
        app.teardown_appcontext(self.teardown)
        app.add_url_rule("/pf-swagger-json", "pf-swagger-json", self.swagger_json)
        app.add_url_rule("/pf-swagger-ui", "pf-swagger-ui", self.swagger_ui)

    def teardown(self, exception):
        pass

    def swagger_json(self):
        return {"key": "value"}

    def swagger_ui(self):
        return {"key": "value"}

    def print_me(self):
        print("Bismillah")
        return "Flask PFMarshmallowSwagger Extension"

