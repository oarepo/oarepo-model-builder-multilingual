import marshmallow as ma
from invenio_records_resources.services.records.schema import (
    BaseRecordSchema as InvenioBaseRecordSchema,
)
from marshmallow import fields as ma_fields
from oarepo_runtime.i18n.schema import I18nStrField, MultilingualField


class ModelMetadataSchema(ma.Schema):
    """ModelMetadataSchema schema."""

    a = MultilingualField(I18nStrField())


class ModelSchema(InvenioBaseRecordSchema):
    """ModelSchema schema."""

    metadata = ma_fields.Nested(lambda: ModelMetadataSchema())
