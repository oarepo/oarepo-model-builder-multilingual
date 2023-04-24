from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records.systemfields import ConstantField
from invenio_records_resources.records.api import Record
from invenio_records_resources.records.systemfields import IndexField
from invenio_records_resources.records.systemfields.pid import PIDField, PIDFieldContext
from model.records.dumper import ModelDumper
from model.records.models import ModelMetadata
from model.records.multilingual_dumper import MultilingualDumper


class ModelIdProvider(RecordIdProviderV2):
    pid_type = "model"


class ModelRecord(Record):
    model_cls = ModelMetadata

    schema = ConstantField("$schema", "local://model-1.0.0.json")

    index = IndexField("model-model-1.0.0")

    pid = PIDField(provider=ModelIdProvider, context_cls=PIDFieldContext, create=True)

    dumper_extensions = [MultilingualDumper()]
    dumper = ModelDumper(extensions=dumper_extensions)
