import re

import marshmallow as ma
from marshmallow import ValidationError, fields, validates
from oarepo_model_builder.datatypes import DataTypeComponent


def validate_fields(labels):
    pattern = re.compile(r"^(label|help).[a-zA-Z]{2}$")

    for key, value in labels.items():
        if not pattern.match(key):
            raise ValidationError(
                f"Invalid key '{key}'. Keys must match pattern 'label.xy' or 'help.xy'."
            )
        if not isinstance(value, str):
            raise ValidationError(
                f"Invalid value for key '{key}'. Values must be strings."
            )


class LangDefField(fields.Field):
    pass


class ValueDefField(fields.Field):
    pass


class MultilingualSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    @validates("lang_def")
    def validate_lang_schema(self, data, **kwargs):
        validate_fields(data)

    @validates("value_def")
    def validate_value_schema(self, data, **kwargs):
        validate_fields(data)

    lang_field = fields.String(data_key="lang-field", required=False)
    value_field = fields.String(data_key="value-field", required=False)
    lang_def = LangDefField()
    value_def = ValueDefField()
    i18n = fields.Boolean(required=False)
    usei18n = fields.Boolean(required=False)


class RegularMultilingualComponent(DataTypeComponent):
    class ModelSchema(ma.Schema):
        multilingual = ma.fields.Nested(
            MultilingualSchema,
            required=False,
        )
