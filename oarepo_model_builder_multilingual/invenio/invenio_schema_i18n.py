from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioSchemaI18nStrBuilder(InvenioBaseClassPythonBuilder):
    TYPE = 'invenio_schema_i18n'
    class_config = 'i18n-schema-class'
    template = 'subschema-i18n'
