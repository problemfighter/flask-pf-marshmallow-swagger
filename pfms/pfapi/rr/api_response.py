from pfms.pfapi.pfms_cons import SUCCESS, SUCCESS_CODE
from pfms.pfapi.rr.data_response import DataResponse
from pfms.pfapi.rr.base_response import MessageResponse


def data_response(data, status=SUCCESS):
    dr = DataResponse(data)
    dr.status = status
    dr.code = SUCCESS_CODE
    return dr


def message_response(message, status=SUCCESS, code=SUCCESS_CODE):
    mr = MessageResponse()
    mr.status = status
    mr.code = code
    mr.message = message
    return mr
