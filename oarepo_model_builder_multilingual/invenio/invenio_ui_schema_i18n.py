from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioUISchemaI18nStrBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_ui_schema_i18n"
    class_config = "i18n-ui-schema-class"
    template = "ui-subschema-i18n"