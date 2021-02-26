from pfms.pfapi.pfms_cons import SUCCESS, SUCCESS_CODE
from pfms.pfapi.rr.data_response import DataResponse
from pfms.pfapi.rr.base_response import MessageResponse


def data_response(data, status=SUCCESS):
    return bulk_data_response(data, status, False)


def bulk_success_data_response(data):
    return bulk_data_response(data)


def bulk_data_response(data, status=SUCCESS, many=True):
    dr = DataResponse().set_data(data, many)
    dr.status = status
    dr.code = SUCCESS_CODE
    return dr


def message_response(message, status=SUCCESS, code=SUCCESS_CODE):
    mr = MessageResponse()
    mr.status = status
    mr.code = code
    mr.message = message
    return mr
