import enum
from marshmallow import ValidationError, fields


class BaseEnum(enum.Enum):

    @classmethod
    def values(cls) -> list:
        return list(map(lambda c: c.value, cls))

    @classmethod
    def keys(cls) -> list:
        return list(map(lambda c: c.name, cls))

    @classmethod
    def to_map(cls) -> dict:
        data = {}
        for enum_type in cls:
            data[enum_type.name] = enum_type.value
        return data

    @classmethod
    def value_to_key(cls, value):
        for enum_type in cls:
            if enum_type.value == value:
                return enum_type.name
        return None

    def __str__(self):
        return self.value

    def is_pfenum(self):
        return True


def validate_enum_value(values: list, value: str, key: str, message: str = "Value should be any of "):
    if value not in values:
        message += '(' + ', '.join(values) + ')'
        raise ValidationError(message, key)


class EnumField(fields.String):
    enumType: BaseEnum

    def __init__(self, enumType, *args, **kwargs):
        self.enumType = enumType
        super(EnumField, self).__init__(*args, **kwargs)

    def _serialize(self, value, attr, obj, **kwargs):
        if isinstance(value, enum.Enum):
            return value.value
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        if hasattr(self.enumType, 'is_pfenum'):
            validate_enum_value(self.enumType.values(), data[attr], attr)
        name = self.enumType.value_to_key(data[attr])
        return self.enumType[name]
