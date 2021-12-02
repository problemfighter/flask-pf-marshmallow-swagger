from fpf_common.common.pff_common_exception import PFFCommonException
from flask import make_response
from pfms.common.pfms_exception import PfMsException
from pfms.pfapi.base.pfms_base_schema import PfBaseSchema
from pfms.pfapi.pfms_cons import SUCCESS_CODE, ERROR_CODE, SUCCESS, ERROR, APP_JSON, CONTENT_TYPE
from pfms.pfapi.rr.base_response import MessageResponse, ErrorResponse, BaseResponse, DataResponse, Pagination


class PfResponseProcessor:

    def flask_json_response(self, json_string: str, code=200):
        response = make_response(
            json_string,
            code
        )
        response.headers[CONTENT_TYPE] = APP_JSON
        return response

    def json_response(self, response: BaseResponse, many=False, http_code=200):
        return self.flask_json_response(response.json(many), code=http_code)

    def message_response(self, message, status, code) -> MessageResponse:
        response = MessageResponse()
        response.status = status
        response.code = code
        response.message = message
        return response

    def success(self, message, code=SUCCESS_CODE, http_code=200):
        return self.json_response(self.message_response(message, SUCCESS, code), http_code=http_code)

    def error(self, message, code=ERROR_CODE, http_code=200):
        return self.json_response(self.message_response(message, ERROR, code), http_code=http_code)

    def error_response(self, errors: dict, message=None, status=ERROR, code=ERROR_CODE):
        response = ErrorResponse()
        response.status = status
        response.code = code
        response.error = errors
        response.message = message
        return self.json_response(response)

    def _data_response(self, data, many=False, pf_schema: PfBaseSchema = None, pagination=None):
        response: DataResponse = DataResponse()
        response.status = SUCCESS
        response.code = SUCCESS_CODE
        if pf_schema:
            data = pf_schema.dump(data, many=many)
        response.add_data(data, many)
        if pagination:
            pagination_string = Pagination().dump(pagination)
            response.add_pagination(pagination_string)
        return self.json_response(response, False)

    def data_response(self, data, pf_schema: PfBaseSchema = None, many=False):
        return self._data_response(data, many, pf_schema)

    def list_dic_data_response(self, data_list_dic, many=False):
        response: DataResponse = DataResponse()
        response.status = SUCCESS
        response.code = SUCCESS_CODE
        response.add_data(data_list_dic, many)
        return self.json_response(response, False)

    def dictionary_data_response(self, data_dict, many=False):
        response: DataResponse = DataResponse()
        response.status = SUCCESS
        response.code = SUCCESS_CODE
        response.add_data(data_dict, many)
        return self.json_response(response, many)

    def bulk_data_response(self, data, pf_schema: PfBaseSchema = None):
        return self._data_response(data, True, pf_schema)

    def data_list_response(self, data, pf_schema: PfBaseSchema):
        return self._data_response(data, True, pf_schema)

    def paginated_data_response(self, data, pf_schema: PfBaseSchema = None):
        pagination = Pagination()
        pagination.page = data.page
        pagination.totalPage = data.pages
        pagination.itemPerPage = data.per_page
        pagination.total = data.total
        return self._data_response(data.items, True, pf_schema, pagination)

    def handle_global_exception(self, pfms_exception: PfMsException):
        if pfms_exception.error_response:
            return pfms_exception.error_response
        elif pfms_exception.message_response:
            return pfms_exception.message_response
        elif pfms_exception.message:
            return self.error(pfms_exception.message)
        else:
            return self.error("Unknown Error")

    def handle_common_exception(self, exception: PFFCommonException):
        message = str(exception)
        if message:
            return self.error(message)
        else:
            return self.error("Unknown Error")


pf_response = PfResponseProcessor()
