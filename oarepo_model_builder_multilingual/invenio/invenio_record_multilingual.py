from oarepo_model_builder.datatypes import DataType
from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder

OAREPO_SORTABLE_PROPERTY = "sortable"


class InvenioRecordMultilingualBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_multilingual"
    section = "record"
    template = "record-multilingual"
