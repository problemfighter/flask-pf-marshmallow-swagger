from pfms.pfapi.pfms_cons import SUCCESS
from pfms.pfapi.rr.data_response import DataResponse


def data_response(data, status=SUCCESS):
    dr = DataResponse(data)
    dr.status = status
    return dr
