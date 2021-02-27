from pfms.pfapi.base.pfms_base_schema import PfBaseSchema
from marshmallow import fields


class Details(PfBaseSchema):
    first_name = fields.String(required=True, error_messages={"required": "Please enter first name"})
    last_name = fields.String()
    email = fields.Email(required=True, error_messages={"required": "Please enter email address", "invalid": "Invalid email address."})
