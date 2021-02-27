from flask import Blueprint, render_template
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from pfms.common.pfms_exception import PfMsException
from pfms.pfapi.rr.pfms_response_processor import pf_response
from pfms.swagger.pfms_actions_to_definition import ActionsToSwagger


class PFMarshmallowSwagger:

    _api_specification = APISpec(
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
        app.register_error_handler(PfMsException, self.exception_handling)

    def update_swagger_details(self, title="PF Marshmallow Swagger", version="1.0.0"):
        self._api_specification.title = title
        self._api_specification.version = version

    def swagger_json(self):
        actions_to_swagger = ActionsToSwagger(self.app, self._api_specification)
        actions_to_swagger.process()
        return self._api_specification.to_dict()

    def swagger_ui(self):
        return render_template('pf-swagger-ui.html')

    def exception_handling(self, exception: PfMsException):
        return pf_response.handle_global_exception(exception)


