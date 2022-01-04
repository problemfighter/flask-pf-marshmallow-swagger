from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec.ext.marshmallow.field_converter import FieldConverterMixin
from marshmallow import fields

marshmallow_plugin = MarshmallowPlugin()

pfms_swagger_api_spec = APISpec(
        title="PF Marshmallow Swagger",
        version="1.0.0",
        openapi_version="3.0.2",
        plugins=[marshmallow_plugin]
    )



@marshmallow_plugin.map_to_openapi_type("string", "binary")
class FileUpload(fields.String):
    pass
