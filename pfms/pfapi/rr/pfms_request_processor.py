from flask import request
from marshmallow import ValidationError, EXCLUDE
from pfms.common.pfms_exception import PfMsException
from pfms.pfapi.base.pfms_base_schema import PfBaseSchema
from pfms.pfapi.pfms_cons import VALIDATION_ERROR_CODE, VALIDATION_ERROR_MSG, INVALID_VALIDATION_REQUEST_MSG
from pfms.pfapi.rr.pfms_response_processor import pf_response
from pfms.swagger.pfms_swagger_api_spec import FileUpload
from sqlalchemy import text
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

    def file_data(self):
        files = request.files
        if files:
            return files
        return None

    def get_requested_value(self, key, default=None):
        value = self.get_query_param_value(key, default)
        if not value:
            value = self.get_requested_data_value(key, default)
        if value:
            return value
        return default

    def get_query_param_value(self, key, default=None):
        args = self.query_params()
        if args and key in args:
            return args.get(key)
        return default

    def get_required_query_param_value(self, key, message: str = "Invalid query params", default=None):
        value = self.get_query_param_value(key, default)
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

    def validate_and_process(self, pf_schema: PfBaseSchema, existing_instance=None):
        request_data = self.get_request_data()
        if not request_data:
            raise PfMsException(message=INVALID_VALIDATION_REQUEST_MSG)
        return self.request_validate(request_data, pf_schema, existing_instance)

    def request_validate(self, data, pf_schema: PfBaseSchema, existing_instance=None):
        try:
            return pf_schema.load(data, session=session, instance=existing_instance, unknown=EXCLUDE)
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

    def pagination_params(self):
        page: int = request.args.get('page', type=int)
        if not page:
            page = 0
        per_page: int = request.args.get('per-page', type=int)
        if not per_page:
            per_page = 25
        return {"page": page, "per_page": per_page}

    def add_pagination(self, model):
        pagination = self.pagination_params()
        return model.paginate(page=pagination['page'], per_page=pagination['per_page'], error_out=False)

    def get_search_string(self):
        return self.get_requested_value("search")

    def add_order_by(self, model, default_field="id", default_order="desc"):
        sort_field = self.get_requested_value("sort_field")
        if not sort_field:
            sort_field = default_field

        sort_order = self.get_requested_value("sort_order")
        if not sort_order:
            sort_order = default_order
        elif sort_order and (sort_order != "asc" and sort_order != "desc"):
            sort_order = default_order

        return model.order_by(text(sort_field + " " + sort_order))

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
                if name in files:
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
                form_data[file_name] = name_and_file_dic[file_name]
        return form_data

    def upload_request_validate(self, pf_schema: PfBaseSchema, existing_instance=None):
        form_data = self._adjust_file_name_with_request(pf_schema)
        return self.request_validate(form_data, pf_schema, existing_instance)
