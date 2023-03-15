import langcodes
from marshmallow import INCLUDE, ValidationError, fields, validates_schema
from oarepo_model_builder.validation.utils import ExtendablePartSchema


class SupportedLangs(ExtendablePartSchema):
    class Meta:
        unknown = INCLUDE

    @validates_schema
    def validate_schema(self, data, **kwargs):
        for lang in data:
            if not langcodes.Language.get(lang).is_valid():
                raise ValidationError("Invalid language code")


class PropertyMultilingual(ExtendablePartSchema):
    i18n = fields.Boolean(required=False)
    usei18n = fields.Boolean(required=False)
    sortable = fields.Boolean(required=False)
    lang_field = fields.String(data_key="lang-field", required=False)
    value_field = fields.String(data_key="value-field", required=False)


class Property(ExtendablePartSchema):
    multilingual = fields.Nested(nested=PropertyMultilingual(), required=False)


class SettingsSchema(ExtendablePartSchema):
    # supported_langs = fields.Nested(
    #     data_key="supported-langs", required=False, nested=SupportedLangs()
    # )
    supported_langs = fields.Raw(data_key="supported-langs", required=False)


class ModelDefaults(ExtendablePartSchema):
    multilingual_dumper_class = fields.String(
        data_key="multilingual-dumper-class", required=False
    )
    multilingual_schema_class = fields.String(
        data_key="multilingual-schema-class", required=False
    )
    i18n_schema_class = fields.String(data_key="i18n-schema-class", required=False)

    i18n_ui_schema_class = fields.String(
        data_key="i18n-ui-schema-class", required=False
    )
    multilingual_ui_schema_class = fields.String(
        data_key="multilingual-ui-schema-class", required=False
    )


validators = {
    "settings": SettingsSchema,
    "model": ModelDefaults,
    "property-multilingual": PropertyMultilingual,
    "property": [Property],
}
