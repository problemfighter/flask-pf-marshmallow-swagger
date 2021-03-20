from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from pf_sqlalchemy.db.orm import BaseModel


class PfBaseSchema(SQLAlchemySchema):
    pass


class PfDetailBaseSchema(PfBaseSchema):
    class Meta:
        model = BaseModel

    id = auto_field()
    created = auto_field()
    updated = auto_field()
    uuid = auto_field()


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
