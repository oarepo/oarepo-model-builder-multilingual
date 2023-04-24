import marshmallow as ma
from marshmallow import fields as ma_fields
from oarepo_runtime.i18n.ui_schema import I18nStrUIField, MultilingualUIField
from oarepo_runtime.ui.marshmallow import InvenioUISchema


class ModelMetadataUISchema(ma.Schema):
    """ModelMetadataUISchema schema."""

    a = MultilingualUIField(I18nStrUIField())


class ModelUISchema(InvenioUISchema):
    """ModelUISchema schema."""

    metadata = ma_fields.Nested(lambda: ModelMetadataUISchema())
