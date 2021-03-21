from pfms.swagger.pfms_swagger_cons import APPLICATION_JSON


class PFMSDefinition:
    url: str = None
    path_params = None
    request_body = None
    response_obj = None
    response_type = APPLICATION_JSON
    request_type = APPLICATION_JSON
    response_exclude = None
    request_exclude = None
    query_param = None
    error_details = None
    only_message: bool = False
    rr_type = None
    methods = []
    tags = []

    response_component: str = None
    request_component: str = None
    description: str = ""

