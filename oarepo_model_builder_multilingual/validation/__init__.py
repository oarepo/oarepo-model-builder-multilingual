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


class LanguagesSettingsSchema(ExtendablePartSchema):
    supported_langs = fields.Raw(
        data_key="supported-langs", attribute="supported-langs", required=False
    )


validators = {
    "settings": LanguagesSettingsSchema,
}
