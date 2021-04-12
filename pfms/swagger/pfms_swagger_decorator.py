from functools import wraps

from pfms.common.pfms_data_type import integer, string
from pfms.swagger.pfms_definition import PFMSDefinition
from pfms.swagger.pfms_swagger_cons import CREATE_UPDATE, LIST, CREATE, SIMPLE_GET, BULK_CREATE, DETAILS, DELETE, \
    PAGINATED_LIST, POST, BINARY_UPLOAD


def request_response(rr_type,
        request_body=None, response_obj=None, query_param=None,
        error_details=True, request_type='application/json',
        response_type='application/json', only_message=False):
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
                pfms_definition.only_message = only_message
                return pfms_definition
            return function(*args, **kwargs)
        return pfms_swagger_def
    return decorator


def pfms_post_request(request_body, response_obj=None, only_message=False):
    return request_response(POST, request_body, response_obj, only_message=only_message)


def request_response_list(request_body, response_obj):
    return request_response(LIST, request_body, response_obj)


def simple_get(response_obj, query_param=None):
    return request_response(SIMPLE_GET, response_obj=response_obj, query_param=query_param)


def pfms_create(request_body, response_obj=None, only_message=True):
    return request_response(CREATE, request_body, response_obj, only_message=only_message)


def pfms_details(response_obj):
    return request_response(rr_type=DETAILS, response_obj=response_obj, error_details=False)


def pfms_delete():
    return request_response(rr_type=DELETE, error_details=False, only_message=True)


def pfms_restore():
    return request_response(rr_type=DELETE, error_details=False, only_message=True)


def bulk_create(request_body, response_obj):
    return request_response(BULK_CREATE, request_body, response_obj)


def pfms_pagination_list(response_obj, query_param: list = None):
    if not query_param:
        query_param = []
    query_param.append(("page", integer))
    query_param.append(("per-page", integer))
    return request_response(PAGINATED_LIST, response_obj=response_obj, query_param=query_param)


def pfms_pagination_sort_list(response_obj, query_param: list = None):
    if not query_param:
        query_param = []
    query_param.append(("sort-field", string))
    query_param.append(("sort-order", string))
    return pfms_pagination_list(response_obj, query_param)


def pfms_pagination_sort_search_list(response_obj, query_param: list = None):
    if not query_param:
        query_param = []
    query_param.append(("search", string))
    return pfms_pagination_sort_list(response_obj, query_param)


def pfms_binary_upload(request_body, response_obj):
    return request_response(BINARY_UPLOAD, request_body, response_obj)
