import re

import marshmallow as ma
from marshmallow import ValidationError, fields, validates
from oarepo_model_builder.datatypes import DataTypeComponent


def validate_fileds(labels):
    pattern = re.compile(r"^(lang|value)_[a-zA-Z]{2}$")

    for key, value in labels.items():
        if not pattern.match(key):
            raise ValidationError(
                f"Invalid key '{key}'. Keys must match pattern 'lang_xy' or 'value_xy'."
            )
        if not isinstance(value, str):
            raise ValidationError(
                f"Invalid value for key '{key}'. Values must be strings."
            )


class LabelsField(fields.Field):
    pass


class HelpsField(fields.Field):
    pass


class MultilingualSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    @validates("labels")
    def validate_labels_schema(self, data, **kwargs):
        validate_fileds(data)

    @validates("helps")
    def validate_helps_schema(self, data, **kwargs):
        validate_fileds(data)

    lang_field = fields.String(data_key="lang-field", required=False)
    value_field = fields.String(data_key="value-field", required=False)
    labels = LabelsField()
    helps = HelpsField()
    i18n = fields.Boolean(required=False)
    usei18n = fields.Boolean(required=False)


class RegularMultilingualComponent(DataTypeComponent):
    class ModelSchema(ma.Schema):
        multilingual = ma.fields.Nested(
            MultilingualSchema,
            required=False,
        )
