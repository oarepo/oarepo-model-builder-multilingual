from oarepo_model_builder.invenio.invenio_record_schema import (
    InvenioRecordSchemaBuilder,
)
from oarepo_model_builder.property_preprocessors import PropertyPreprocessor, process
from oarepo_model_builder.stack import ModelBuilderStack, ReplaceElement
from oarepo_model_builder.utils.camelcase import camel_case
from oarepo_model_builder.utils.deepmerge import deepmerge


class I18nStrPreprocessor(PropertyPreprocessor):

    @process(
        model_builder=InvenioRecordSchemaBuilder,
        path="/properties/**",
        condition=lambda current, stack: current.type == "i18nStr",
    )
    def modify_multilang_marshmallow(self, data, stack: ModelBuilderStack, **kwargs):
        definition = data.get("multilingual", {})
        use_i18n = False
        if "usei18n" in definition:
            use_i18n = True
        lang = definition.get("lang-field", "lang")
        value = definition.get("value-field", "value")
        properties = data.get("properties", {})
        if lang == "lang" and value == "value" and not use_i18n:
            data["type"] = "object"
            deepmerge(
                data.setdefault("marshmallow", {}),
                {"schema-class": self.schema.current_model.i18n_schema_class, "generate": False},
            )
        else:
            data["type"] = "object"
            data["properties"] = {
                lang: {"type": "keyword", "required": True},
                value: {"type": "keyword", "required": True},
                **properties,
            }
            if "marshmallow" in data and "class" in data["multilingual"]:
                class_name = data["marshmallow"]["class"]
            else:
                class_name = camel_case(stack.top.key) + "Schema"
            deepmerge(
                data.setdefault("marshmallow", {}),
                {
                    "generate": True,
                    "class": class_name,
                    # "nested": True,
                    "validates": {
                        lang: {
                            "imports": ["import langcodes"],
                            "definition": """def validate_lang(self, value):
                                    if value != "_" and not langcodes.Language.get(value).is_valid():
                                        raise ma_ValidationError("Invalid language code")""",
                        }
                    },
                },
            )

        return data
