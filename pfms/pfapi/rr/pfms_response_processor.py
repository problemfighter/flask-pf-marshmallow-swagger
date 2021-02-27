from flask import make_response
from marshmallow import fields
from pfms.common.pfms_exception import PfMsException
from pfms.pfapi.pfms_cons import SUCCESS_CODE, ERROR_CODE, SUCCESS, ERROR, APP_JSON, CONTENT_TYPE
from pfms.pfapi.rr.base_response import MessageResponse, ErrorResponse, BaseResponse, DataResponse


class PfResponseProcessor:

    def flask_json_response(self, json_string: str, code=200):
        response = make_response(
            json_string,
            code
        )
        response.headers[CONTENT_TYPE] = APP_JSON
        return response

    def json_response(self, response: BaseResponse, many=False):
        return self.flask_json_response(response.json(many))

    def message_response(self, message, status, code) -> MessageResponse:
        response = MessageResponse()
        response.status = status
        response.code = code
        response.message = message
        return response

    def success(self, message, code=SUCCESS_CODE):
        return self.json_response(self.message_response(message, SUCCESS, code))

    def error(self, message, code=ERROR_CODE):
        return self.json_response(self.message_response(message, ERROR, code))

    def error_response(self, errors: dict, message=None, status=ERROR, code=ERROR_CODE):
        response = ErrorResponse()
        response.status = status
        response.code = code
        response.error = errors
        response.message = message
        return self.json_response(response)

    def _data_response(self, data, many=False):
        response: DataResponse = DataResponse()
        response.status = SUCCESS
        response.code = SUCCESS_CODE
        response.add_data(data, many)
        return self.json_response(response, False)

    def data_response(self, data):
        return self._data_response(data)

    def bulk_data_response(self, data):
        return self._data_response(data, True)

    def handle_global_exception(self, pfms_exception: PfMsException):
        if pfms_exception.error_response:
            return pfms_exception.error_response
        elif pfms_exception.message_response:
            return pfms_exception.message_response
        elif pfms_exception.message:
            return self.error(pfms_exception.message)
        else:
            return self.error("Unknown Error")


pf_response = PfResponseProcessor()
