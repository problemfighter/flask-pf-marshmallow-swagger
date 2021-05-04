from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from pf_sqlalchemy.db.orm import BaseModel


class PfOnlySchema(Schema):
    pass


class PfBaseSchema(SQLAlchemySchema):
    pass


class PfDetailBaseSchema(PfBaseSchema):
    class Meta:
        model = BaseModel

    id = auto_field()
    created = auto_field()
    updated = auto_field()
    uuid = auto_field()
    isActive = auto_field()


class ModelViewSort(Schema):
    id = fields.Integer(required=True, error_messages={"required": "Please enter entity id."})
    viewOrder = fields.Integer(required=True, error_messages={"required": "Please enter view order."})


def common_exclude():
    exclude = ["id", "created", "updated", "uuid"]
    return exclude


def update_exclude():
    exclude = ("created", "updated", "uuid")
    return exclude


def common_exclude_append(*args):
    list_args = list(args)
    list_args.extend(common_exclude())
    return list_args


def update_exclude_append(*args):
    list_args = list(args)
    list_args.extend(update_exclude())
    return list_args
