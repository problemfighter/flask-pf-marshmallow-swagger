from pfms.pfapi.rr.base_request import BaseRequest


def single_request(data):
    sr = BaseRequest(data)
    return sr


def bulk_request(data):
    br = BaseRequest(data, True)
    return br
