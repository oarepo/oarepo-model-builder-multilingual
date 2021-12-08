

import langcodes
from marshmallow import Schema, fields, ValidationError, validates_schema, INCLUDE, validate



class MultilingualSchema(Schema):
    lang = fields.String(required=True)
    value = fields.String(required=True)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        print(data)
        lang_val = data.get('lang', None)
        print(lang_val)
        if lang_val != '_' and not langcodes.Language.get(lang_val).is_valid():
            raise ValidationError(lang_val, "Wrong data type")

