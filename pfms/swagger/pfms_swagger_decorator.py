from functools import wraps

from pfms.swagger.pfms_definition import PFMSDefinition
from pfms.swagger.pfms_swagger_cons import CREATE_UPDATE, LIST, CREATE, SIMPLE_GET, BULK_CREATE


def request_response(rr_type,
        request_body=None, response_obj=None, query_param=None,
        error_details=True, request_type='application/json',
        response_type='application/json'):
    def decorator(function):
        function.__pfms__ = "PFMS"

        @wraps(function)
        def pfms_swagger_def(*args, **kwargs):
            if 'pfms_definition' in kwargs and kwargs['pfms_definition']:
                pfms_definition = PFMSDefinition()
                pfms_definition.request_body = request_body
                pfms_definition.response_obj = response_obj
                pfms_definition.response_type = response_type
                pfms_definition.error_details = error_details
                pfms_definition.query_param = query_param
                pfms_definition.rr_type = rr_type
                pfms_definition.request_type = request_type
                return pfms_definition
            return function(*args, **kwargs)
        return pfms_swagger_def
    return decorator


def request_response_list(request_body, response_obj):
    return request_response(LIST, request_body, response_obj)


def simple_get(response_obj, query_param=None):
    return request_response(SIMPLE_GET, response_obj=response_obj, query_param=query_param)


def pfms_create(request_body, response_obj):
    return request_response(CREATE, request_body, response_obj)


def bulk_create(request_body, response_obj):
    return request_response(BULK_CREATE, request_body, response_obj)

