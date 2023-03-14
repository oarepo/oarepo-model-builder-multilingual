from oarepo_model_builder.builders.mapping import MappingBuilder
from oarepo_model_builder.datatypes import datatypes, ArrayDataType
from oarepo_model_builder.invenio.invenio_record_schema import (
    InvenioRecordSchemaBuilder,
)
from oarepo_model_builder.property_preprocessors import PropertyPreprocessor, process
from oarepo_model_builder.stack import ModelBuilderStack, ReplaceElement
from oarepo_model_builder.utils.camelcase import camel_case
from oarepo_model_builder.utils.deepmerge import deepmerge

from oarepo_model_builder_multilingual.datatypes import I18nDataType
from oarepo_model_builder_multilingual.utils.supported_langs import alternative_gen

def neco(object, data, key):
    alternative = alternative_gen(object.settings['supported-langs'], key)
    definition = data.get('multilingual', {})

    lang = definition.get('lang-field', 'lang')
    value = definition.get('value-field', 'value')
    properties = data.get('properties', {})

    data = {
        key: {
            'type': 'object',
            'properties': {
                lang: {
                    'type': 'keyword'

                },
                value: {
                    'type': 'fulltext+keyword'
                }, **properties
            }
        }
    }

    deepmerge(data, alternative)
    return data

class I18nStrPreprocessor(PropertyPreprocessor):
    @process(model_builder=MappingBuilder,
             path="/properties/**",
             condition=lambda current, stack: current.top.is_schema_valid)
    def modify_multilang_mapping(self, data, stack: ModelBuilderStack, **kwargs):
        if stack.top.schema_element_type == 'property':
            d_type = datatypes.get_datatype(
                stack.top.data,
                stack.top.key,
                self.schema.current_model,
                self.schema,
                stack,
            )
            if isinstance(d_type, I18nDataType):
                data = neco(self, data, stack.top.key)
                raise ReplaceElement(data)

            elif isinstance(d_type, ArrayDataType):
                stack.push('items', stack.top.data['items'])
                d_type = datatypes.get_datatype(
                    stack.top.data,
                    stack.top.key,
                    self.schema.current_model,
                    self.schema,
                    stack,
                )
                if isinstance(d_type, I18nDataType):
                    data = neco(self, data, stack[-2].key)
                    stack.pop()
                    raise ReplaceElement(data)
                stack.pop()


    # @process(
    #     model_builder=InvenioRecordSchemaBuilder,
    #     path="/properties/**",
    #     condition=lambda current, stack: current.type == "i18nStr",
    # )
    # def modify_multilang_marshmallow(self, data, stack: ModelBuilderStack, **kwargs):
    #     definition = data.get("multilingual", {})
    #     use_i18n = False
    #     if "usei18n" in definition:
    #         use_i18n = True
    #     lang = definition.get("lang-field", "lang")
    #     value = definition.get("value-field", "value")
    #     properties = data.get("properties", {})
    #     if lang == "lang" and value == "value" and not use_i18n:
    #         data["type"] = "object"
    #         deepmerge(
    #             data.setdefault("marshmallow", {}),
    #             {"schema-class": self.schema.current_model.i18n_schema_class, "generate": False},
    #         )
    #         deepmerge(
    #             data.setdefault("ui", {}),
    #             {"marshmallow": {"schema-class": self.schema.current_model.i18n_ui_schema_class, "generate": False}},
    #         )
    #     else:
    #         data["type"] = "object"
    #         data["properties"] = {
    #             lang: {"type": "keyword", "required": True},
    #             value: {"type": "keyword", "required": True},
    #             **properties,
    #         }
    #         if "marshmallow" in data and "class" in data["multilingual"]:
    #             class_name = data["marshmallow"]["class"]
    #         else:
    #             class_name = camel_case(stack.top.key) + "Schema"
    #         deepmerge(
    #             data.setdefault("marshmallow", {}),
    #             {
    #                 "generate": True,
    #                 "schema-class": class_name,
    #                 "nested": True,
    #                 "validates": {
    #                     lang: {
    #                         "imports": ["import langcodes"],
    #                         "definition": """def validate_lang(self, value):
    #                                 if value != "_" and not langcodes.Language.get(value).is_valid():
    #                                     raise ma_ValidationError("Invalid language code")""",
    #                     }
    #                 },
    #             },
    #         )
    #
    #     return data
