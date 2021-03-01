from flask import request
from marshmallow import ValidationError
from pfms.common.pfms_exception import PfMsException
from pfms.pfapi.base.pfms_base_schema import PfBaseSchema
from pfms.pfapi.pfms_cons import VALIDATION_ERROR_CODE, VALIDATION_ERROR_MSG, INVALID_VALIDATION_REQUEST_MSG
from pfms.pfapi.rr.pfms_response_processor import pf_response
from sqlalchemy.orm import session


class PfRequestProcessor:

    def json_data(self):
        json = request.get_json()
        if json:
            return json
        return None

    def get_request_data(self):
        json = self.json_data()
        if json and isinstance(json, dict) and "data" in json:
            return json['data']
        return None

    def validate_and_process(self, pf_schema: PfBaseSchema):
        request_data = self.get_request_data()
        if not request_data:
            raise PfMsException(message=INVALID_VALIDATION_REQUEST_MSG)
        return self.request_validate(request_data, pf_schema)

    def request_validate(self, json, pf_schema: PfBaseSchema):
        try:
            return pf_schema.load(json, session=session)
        except ValidationError as error:
            error_dic = self._process_validation_error(error)
            error_exception = pf_response.error_response(errors=error_dic, code=VALIDATION_ERROR_CODE, message=VALIDATION_ERROR_MSG)
            raise PfMsException(error_response=error_exception)

    def _process_validation_error(self, error: ValidationError):
        message_dict: dict = {}
        if error and error.messages:
            for message in error.messages:
                error_text = ""
                for text in error.messages[message]:
                    error_text += text
                message_dict[message] = error_text
        return message_dict

