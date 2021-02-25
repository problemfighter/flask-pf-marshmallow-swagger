from pfms.pfapi.pfms_cons import SUCCESS, SUCCESS_CODE
from pfms.pfapi.rr.data_response import DataResponse


def data_response(data, status=SUCCESS):
    dr = DataResponse(data)
    dr.status = status
    dr.code = SUCCESS_CODE
    return dr
