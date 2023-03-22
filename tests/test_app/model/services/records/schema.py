import marshmallow as ma
from invenio_records_resources.services.records.schema import (
    BaseRecordSchema as InvenioBaseRecordSchema,
)
from marshmallow import ValidationError
from marshmallow import fields as ma_fields
from marshmallow import validate as ma_validate
from marshmallow_utils import fields as mu_fields
from marshmallow_utils import schemas as mu_schemas
from oarepo_runtime.i18n.schema import I18nSchema
from oarepo_runtime.ui import marshmallow as l10n
from oarepo_runtime.validation import validate_date


class ModelSchema(InvenioBaseRecordSchema):
    """ModelSchema schema."""

    a = ma_fields.List(ma_fields.Nested(lambda: I18nSchema()))
    created = ma_fields.String(validate=[validate_date("%Y-%m-%d")], dump_only=True)
    updated = ma_fields.String(validate=[validate_date("%Y-%m-%d")], dump_only=True)
