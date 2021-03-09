from marshmallow import fields
from pfms.pfapi.pfms_cons import SUCCESS, SUCCESS_CODE
from pfms.pfapi.rr.base_response import MessageResponse, BaseResponse, Pagination


def data_response_def(data, status=SUCCESS):
    return bulk_data_response_def(data, status, False)


def bulk_success_data_response_def(data):
    return bulk_data_response_def(data)


def bulk_data_response_def(data, status=SUCCESS, many=True):
    dr = BaseResponse()
    response = {
        "data": fields.Nested(data, many=many)
    }
    dr.status = status
    return dr.get_data_response_def(response)


def paginated_response_def(data, status=SUCCESS):
    dr = BaseResponse()
    response = {
        "data": fields.Nested(data, many=True),
        "pagination": fields.Nested(Pagination)
    }
    dr.status = status
    return dr.get_data_response_def(response)


def message_response(message, status=SUCCESS, code=SUCCESS_CODE):
    mr = MessageResponse()
    mr.status = status
    mr.code = code
    mr.message = message
    return mr
