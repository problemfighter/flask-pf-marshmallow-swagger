from flask import Blueprint, render_template
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

class PFMarshmallowSwagger():

    __api_specification = APISpec(
        title="PF Marshmallow Swagger",
        version="1.0.0",
        openapi_version="3.0.2",
        plugins=[MarshmallowPlugin()]
    )

    def __init__(self, app=None):
        self.app = app
        self.blue_print = Blueprint("PFMarshmallowSwagger", __name__, template_folder="templates", static_folder="pf-marshmallow-swagger")
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.blue_print.add_url_rule("/pf-swagger-json", "pf-swagger-json", self.swagger_json)
        self.blue_print.add_url_rule("/pf-swagger-ui", "pf-swagger-ui", self.swagger_ui)
        app.register_blueprint(self.blue_print)


    def swagger_json(self):
        return self.__api_specification.to_dict()

    def swagger_ui(self):
        return render_template('pf-swagger-ui.html')

    def print_me(self):
        print("Bismillah")
        return "Flask PFMarshmallowSwagger Extension"

