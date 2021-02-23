
class PFMSDefinition:
    url: str = None
    path_params = None
    request_body = None
    response_obj = None
    response_type = 'application/json'
    request_type = 'application/json'
    response_exclude = None
    request_exclude = None
    query_param = None
    error_details = None
    rr_type = None
    methods = []

