from marshmallow import Schema, fields


def single_request(data):
    sr = Schema.from_dict({
        "data": fields.Nested(data)
    })
    return sr


def bulk_request(data):
    br = Schema.from_dict({
        "data": fields.Nested(data)
    })
    return br
