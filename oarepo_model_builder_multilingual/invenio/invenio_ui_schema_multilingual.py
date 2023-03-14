from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioUISchemaMultilingualBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_ui_schema_multilingual"
    class_config = "multilingual-ui-schema-class"
    template = "ui-subschema-multilingual"
