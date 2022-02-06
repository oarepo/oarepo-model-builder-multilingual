from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioSchemaMultilingualBuilder(InvenioBaseClassPythonBuilder):
    TYPE = 'invenio_schema_multilingual'
    class_config = 'multilingual-schema-class'
    template = 'subschema-multilingual'
