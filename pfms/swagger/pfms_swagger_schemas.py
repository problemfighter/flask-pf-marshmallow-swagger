from pfms.swagger.pfms_definition import PFMSDefinition

IN_PATH = "path"
IN_QUERY = "query"
OBJ = "object"
ARRAY = "array"


def get_parameter(place, name, data_type, required=False):
    return {
        "name": name,
        "in": place,
        "schema": {
            "type": data_type
        },
        "required": required
    }


def get_component_schemas_link(name):
    return "#/components/schemas/" + name


def get_schema_def_ref(ref, s_type=None):
    schema = {"type": s_type}
    if s_type == ARRAY:
        schema["items"] = {
            "$ref": get_component_schemas_link(ref)
        }
        return schema
    return {"$ref": get_component_schemas_link(ref)}


def get_request_body(definition: PFMSDefinition, is_bulk=False):
    s_type = None
    if is_bulk:
        s_type = ARRAY
    return {
        "required": True,
        "content": {
            definition.response_type: {
                "schema": get_schema_def_ref(definition.request_component, s_type)
            }
        }
    }


def get_response(definition: PFMSDefinition, http_code=200):
    return {
        http_code: {
            "content": {
                definition.response_type: {
                    "schema": {

                    }
                }
            }
        }
    }


def get_spec_from_definition():
    pass