from functools import wraps


def request_response(request_body, response_obj, query_param=None, error_details=True, request_type = 'application/json', response_type = 'application/json'):
    pass


def create_update(request_body, response_obj, error_details=True, request_type = 'application/json', response_type = 'application/json'):
    def decorator(function):
        def pfms_swagger_def(*args, **kwargs):
            if 'pfms_definition' in kwargs and kwargs['pfms_definition']:
                return "Create Update Decorator "
            return function(*args, **kwargs)
        return pfms_swagger_def
    return decorator

