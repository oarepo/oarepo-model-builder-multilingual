import marshmallow as ma
from invenio_records_resources.services.records.schema import (
    BaseRecordSchema as InvenioBaseRecordSchema,
)
from marshmallow import ValidationError
from marshmallow import fields as ma_fields
from marshmallow import validate as ma_validate
from marshmallow_utils import fields as mu_fields
from marshmallow_utils import schemas as mu_schemas
from oarepo_runtime.i18n.schema import I18nStrField, MultilingualField
from oarepo_runtime.ui import marshmallow as l10n
from oarepo_runtime.validation import validate_date


class ModelMetadataSchema(ma.Schema):
    """ModelMetadataSchema schema."""

    a = MultilingualField(I18nStrField())


class ModelSchema(InvenioBaseRecordSchema):
    """ModelSchema schema."""

    metadata = ma_fields.Nested(lambda: ModelMetadataSchema())
