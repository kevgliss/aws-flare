import logging
from inflection import underscore

from marshmallow import Schema, SchemaOpts, fields, pre_load
from marshmallow.exceptions import ValidationError


logger = logging.getLogger(__name__)


class DictField(fields.Field):
    def __init__(self, key_field, nested_field, *args, **kwargs):
        fields.Field.__init__(self, *args, **kwargs)
        self.key_field = key_field
        self.nested_field = nested_field

    def _deserialize(self, value, attr, obj):
        ret = {}
        for key, val in value.items():
            k = self.key_field.deserialize(key)
            v = self.nested_field.deserialize(val)
            ret[k] = v
        return ret

    def _serialize(self, value, attr, obj):
        ret = {}
        for key, val in value.items():
            k = self.key_field._serialize(key, attr, obj)
            v = self.nested_field.serialize(key, self.get_value(attr, obj))
            ret[k] = v
        return ret


class OrField(fields.Field):
    def __init__(self, possible_fields, *args, **kwargs):
        fields.Field.__init__(self, *args, **kwargs)
        self.possible_fields = possible_fields

    def _deserialize(self, value, attr, data):
        for field in self.possible_fields:
            try:
                return field.deserialize(value)
            except ValidationError as e:
                logger.exception(e)

    def _serialize(self, value, attr, obj):
        for field in self.possible_fields:
            try:
                return field.serialize(value)
            except ValidationError as e:
                logger.exception(e)


def under(data, many=None):
    items = []
    if many:
        for i in data:
            if isinstance(i, dict):
                items.append(
                    {underscore(key): value for key, value in i.items()}
                )
            else:
                items.append(i)
        return items

    if isinstance(data, dict):
        return {underscore(key): value for key, value in data.items()}

    return data


class FlareOpts(SchemaOpts):
    def __init__(self, meta):
        SchemaOpts.__init__(self, meta)


class FlareSchema(Schema):
    """
    Base schema from which all flare schema's inherit
    """
    OPTIONS_CLASS = FlareOpts

    @pre_load(pass_many=True)
    def pre_process(self, data, many):
        """We need to get the data into a form marshmallow understands"""
        return under(data, many)


def flatten_errors(errors):
    error_list = []

    def _recurse(data, error_list):
        for k, v in data.items():
            if isinstance(v, dict):
                _recurse(v, error_list)
            else:
                error_list += v
    _recurse(errors, error_list)
    return error_list
