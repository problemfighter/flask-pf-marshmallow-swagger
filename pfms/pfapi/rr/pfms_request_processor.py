from flask import request
from marshmallow import ValidationError, EXCLUDE
from pf_file_content.pf_string_util import process_file_name
from pfms.common.pfms_exception import PfMsException
from pfms.pfapi.base.pfms_base_schema import PfBaseSchema
from pfms.pfapi.pfms_cons import VALIDATION_ERROR_CODE, VALIDATION_ERROR_MSG, INVALID_VALIDATION_REQUEST_MSG
from pfms.pfapi.rr.pfms_response_processor import pf_response
from pfms.swagger.pfms_swagger_api_spec import FileUpload
from sqlalchemy.orm import session


class PfRequestProcessor:

    def json_data(self):
        json = request.get_json()
        if json:
            return json
        return None

    def form_data(self):
        data = request.form
        if data:
            return data
        return None

    def query_params(self):
        data = request.args
        if data:
            return data
        return None

    def query_array_param(self, key, default=None, type=None):
        data = request.args.getlist(key, type)
        if data:
            return data
        return default

    def file_data(self):
        files = request.files
        if files:
            return files
        return None

    def get_value_from_request(self, key, default=None):
        value = self.query_params()
        if not value:
            value = self.get_request_data()
        if not value:
            value = self.form_data()
        if not value:
            value = self.file_data()
        if not value:
            return default
        if value and key in value:
            return value.get(key)
        return default

    def get_required_value_from_request(self, key, message: str = "Invalid requested value", default=None):
        value = self.get_value_from_request(key, default)
        if not value:
            raise PfMsException(message=message)
        return value

    def get_requested_value(self, key, default=None, type=None):
        value = self.get_query_param_value(key, default, type)
        if not value:
            value = self.get_requested_data_value(key, default)
        if value:
            return value
        return default

    def get_query_param_value(self, key, default=None, type=None, is_list=False):
        if is_list:
            return self.query_array_param(key, default, type)
        args = self.query_params()
        if args and key in args:
            return args.get(key, type=type)
        return default

    def get_required_query_param_value(self, key, message: str = "Invalid query params", default=None, is_list=False):
        value = self.get_query_param_value(key, default, is_list=is_list)
        if not value:
            raise PfMsException(message=message)
        return value

    def get_required_data_value(self, key, message: str = "Invalid data params", default=None):
        value = self.get_requested_data_value(key, default)
        if not value:
            raise PfMsException(message=message)
        return value

    def get_requested_data_value(self, key, default=None):
        data = self.get_request_data()
        if data and key in data:
            return data.get(key, default)
        return default

    def get_request_data(self):
        json = self.json_data()
        if json and isinstance(json, dict) and "data" in json:
            return json['data']
        return None

    def validate_and_process(self, pf_schema: PfBaseSchema, existing_instance=None, is_validate_only: bool = False):
        request_data = self.get_request_data()
        if not request_data:
            raise PfMsException(message=INVALID_VALIDATION_REQUEST_MSG)
        return self.request_validate(request_data, pf_schema, existing_instance, is_validate_only)

    def request_validate(self, data, pf_schema: PfBaseSchema, existing_instance=None, is_validate_only: bool = False):
        try:
            if is_validate_only:
                response_model = pf_schema.validate(data, session=session)
                if response_model:
                    errors = self._process_only_validation_error(response_model)
                    self._raise_validation_exception(errors)
            else:
                response_model = pf_schema.load(data, session=session, instance=existing_instance, unknown=EXCLUDE)
            return response_model
        except ValidationError as error:
            error_dic = self._process_validation_error(error)
            self._raise_validation_exception(error_dic)

    def _raise_validation_exception(self, errors: dict):
        error_exception = pf_response.error_response(errors=errors, code=VALIDATION_ERROR_CODE, message=VALIDATION_ERROR_MSG)
        raise PfMsException(error_response=error_exception)

    def _process_only_validation_error(self, errors: dict):
        message_dict: dict = {}
        for message in errors:
            error_text = ""
            for text in errors[message]:
                error_text += text + " "
            message_dict[message] = error_text
        return message_dict

    def _process_validation_error(self, error: ValidationError):
        message_dict: dict = {}
        if error and error.messages:
            for message in error.messages:
                error_text = ""
                for text in error.messages[message]:
                    error_text += text + " "
                message_dict[message] = error_text
        return message_dict

    def get_search_string(self):
        return self.get_requested_value("search")

    def get_file_inputs(self, pf_schema: PfBaseSchema) -> list:
        names = []
        for field_name in pf_schema.fields:
            field = pf_schema.fields[field_name]
            if isinstance(field, FileUpload):
                names.append(field.name)
        return names

    def get_uploaded_file_name(self, names: list) -> dict:
        name_and_filename = {}
        if names:
            files = self.file_data()
            for name in names:
                if files and name in files:
                    if files[name].filename != '':
                        name_and_filename[name] = files[name].filename
        return name_and_filename

    def _adjust_file_name_with_request(self, pf_schema: PfBaseSchema):
        form_data = self.form_data()
        form_data = form_data.to_dict(flat=True)
        file_names = self.get_file_inputs(pf_schema)
        name_and_file_dic = self.get_uploaded_file_name(file_names)
        if name_and_file_dic:
            for file_name in name_and_file_dic:
                form_data[file_name] = process_file_name(name_and_file_dic[file_name])
        return form_data

    def remove_null(self, form_data):
        if form_data:
            for key in form_data:
                if key and form_data[key] == 'null':
                    form_data[key] = None
        return form_data

    def upload_request_validate(self, pf_schema: PfBaseSchema, existing_instance=None):
        form_data = self._adjust_file_name_with_request(pf_schema)
        form_data = self.remove_null(form_data)
        return self.request_validate(form_data, pf_schema, existing_instance)
