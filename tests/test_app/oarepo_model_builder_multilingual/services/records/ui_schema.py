import marshmallow as ma
from marshmallow import Schema
from marshmallow import fields as ma_fields
from oarepo_runtime.i18n.ui_schema import I18nStrUIField, MultilingualUIField
from oarepo_runtime.services.schema.ui import InvenioUISchema


class OarepoModelBuilderMultilingualUISchema(InvenioUISchema):
    class Meta:
        unknown = ma.RAISE

    metadata = ma_fields.Nested(
        lambda: OarepoModelBuilderMultilingualMetadataUISchema()
    )


class OarepoModelBuilderMultilingualMetadataUISchema(Schema):
    class Meta:
        unknown = ma.RAISE

    a = MultilingualUIField(I18nStrUIField())
