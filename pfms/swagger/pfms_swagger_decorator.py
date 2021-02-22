from functools import wraps
from pfms.swagger.pfms_swagger_cons import CREATE_UPDATE


def __process_request_response(type, function, request_body, response_obj, query_param=None, error_details=True, request_type='application/json', response_type='application/json', *args, **kwargs):
    if 'pfms_definition' in kwargs and kwargs['pfms_definition']:
        return {
            "request_body": request_body,
            "response_obj": response_obj,
            "response_type": response_type,
            "request_type": request_type,
            "error_details": error_details,
            "query_param": query_param,
            "type": type
        }
    return function(*args, **kwargs)


def request_response(request_body, response_obj, error_details=True, query_param=None, request_type='application/json', response_type='application/json'):
    def decorator(function):
        function.__pfms__ = "PFMS"
        @wraps(function)
        def pfms_swagger_def(*args, **kwargs):
            return __process_request_response(CREATE_UPDATE, function, request_body, response_obj, error_details, query_param, request_type, response_type, *args, **kwargs)
        return pfms_swagger_def
    return decorator
