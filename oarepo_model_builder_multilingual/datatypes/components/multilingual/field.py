import marshmallow as ma
from marshmallow import fields
from oarepo_model_builder.datatypes import DataTypeComponent


class MultilingualSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    lang_name = fields.String(attribute="lang-name", data_key="lang-name", required=False)
    value_name = fields.String(attribute="value-name", data_key="value-name", required=False)
    value_type = fields.String(attribute="value-type", data_key="value-type", required=False)
    value_field = fields.String(attribute="value-field", data_key="value-field", required=False)
    i18n = fields.Boolean(required=False)
    usei18n = fields.Boolean(required=False)


class RegularMultilingualComponent(DataTypeComponent):
    class ModelSchema(ma.Schema):
        multilingual = ma.fields.Nested(
            MultilingualSchema,
            required=False,
        )
