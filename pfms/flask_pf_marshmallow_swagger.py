from flask import Blueprint, render_template
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from pfms.swagger.actions_to_swagger import ActionsToSwagger

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

    def update_swagger_details(self, title = "PF Marshmallow Swagger", version="1.0.0"):
        self.__api_specification.title = title
        self.__api_specification.version = version

    def swagger_json(self):
        actions_to_swagger = ActionsToSwagger(self.app, self.__api_specification)
        actions_to_swagger.process()
        return self.__api_specification.to_dict()

    def swagger_ui(self):
        return render_template('pf-swagger-ui.html')

    def print_me(self):
        print("Bismillah")
        return "Flask PFMarshmallowSwagger Extension"

