import marshmallow as ma
from invenio_records_resources.services.records.schema import (
    BaseRecordSchema as InvenioBaseRecordSchema,
)
from marshmallow import ValidationError
from marshmallow import fields as ma_fields
from marshmallow import validate as ma_validate
from marshmallow_utils import fields as mu_fields
from marshmallow_utils import schemas as mu_schemas
from oarepo_runtime.i18n.ui_schema import I18nStrUIField, MultilingualUIField
from oarepo_runtime.ui import marshmallow as l10n
from oarepo_runtime.ui.marshmallow import InvenioUISchema
from oarepo_runtime.validation import validate_date


class ModelMetadataUISchema(ma.Schema):
    """ModelMetadataUISchema schema."""

    a = MultilingualUIField(I18nStrUIField())


class ModelUISchema(InvenioUISchema):
    """ModelUISchema schema."""

    metadata = ma_fields.Nested(lambda: ModelMetadataUISchema())
    _id = ma_fields.String(data_key="id", attribute="id")
    created = l10n.LocalizedDate()
    updated = l10n.LocalizedDate()
    _schema = ma_fields.String(data_key="$schema", attribute="$schema")
