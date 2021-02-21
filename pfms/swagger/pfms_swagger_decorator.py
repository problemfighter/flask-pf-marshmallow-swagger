from functools import wraps


def request_response():
    pass

def create_update(request_obj, response_obj):
    def decorator(function):
        def pfms_swagger_def(*args, **kwargs):
            if 'pfms_definition' in kwargs and kwargs['pfms_definition']:
                return "Create Update Decorator "
            return function(*args, **kwargs)
        return pfms_swagger_def
    return decorator

