from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records.systemfields import ConstantField
from invenio_records_resources.records.api import Record as InvenioRecord
from invenio_records_resources.records.systemfields import IndexField
from invenio_records_resources.records.systemfields.pid import PIDField, PIDFieldContext

from oarepo_model_builder_multilingual.records.dumpers.dumper import (
    OarepoModelBuilderMultilingualDumper,
)
from oarepo_model_builder_multilingual.records.models import (
    OarepoModelBuilderMultilingualMetadata,
)


class OarepoModelBuilderMultilingualIdProvider(RecordIdProviderV2):
    pid_type = "rpmngl"


class OarepoModelBuilderMultilingualRecord(InvenioRecord):
    model_cls = OarepoModelBuilderMultilingualMetadata

    schema = ConstantField(
        "$schema", "local://oarepo_model_builder_multilingual-1.0.0.json"
    )

    index = IndexField(
        "oarepo_model_builder_multilingual-oarepo_model_builder_multilingual-1.0.0"
    )

    pid = PIDField(
        provider=OarepoModelBuilderMultilingualIdProvider,
        context_cls=PIDFieldContext,
        create=True,
    )

    dumper = OarepoModelBuilderMultilingualDumper()
