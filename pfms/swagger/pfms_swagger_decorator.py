from functools import wraps
from pfms.swagger.pfms_swagger_cons import CREATE_UPDATE


def request_response(request_body, response_obj, query_param=None, error_details=True, request_type = 'application/json', response_type = 'application/json'):
    pass


def create_update(request_body, response_obj, error_details=True, query_param=None, request_type = 'application/json', response_type = 'application/json'):
    def decorator(function):
        def pfms_swagger_def(*args, **kwargs):
            if 'pfms_definition' in kwargs and kwargs['pfms_definition']:
                return {
                    request_body: request_body,
                    response_obj:response_obj,
                    response_type:response_type,
                    request_type:request_type,
                    error_details:error_details,
                    type:CREATE_UPDATE
                }
            return function(*args, **kwargs)
        return pfms_swagger_def
    return decorator

