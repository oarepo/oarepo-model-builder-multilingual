import marshmallow as ma
from marshmallow import Schema
from marshmallow import fields as ma_fields
from oarepo_runtime.i18n.schema import I18nStrField, MultilingualField
from oarepo_runtime.marshmallow import BaseRecordSchema


class OarepoModelBuilderMultilingualSchema(BaseRecordSchema):
    class Meta:
        unknown = ma.RAISE

    metadata = ma_fields.Nested(lambda: OarepoModelBuilderMultilingualMetadataSchema())


class OarepoModelBuilderMultilingualMetadataSchema(Schema):
    class Meta:
        unknown = ma.RAISE

    a = MultilingualField(I18nStrField())
