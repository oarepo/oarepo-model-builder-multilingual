from oarepo_model_builder.builders.mapping import MappingBuilder
from oarepo_model_builder.datatypes import ArrayDataType, datatypes
from oarepo_model_builder.invenio.invenio_record_schema import (
    InvenioRecordSchemaBuilder,
)
from oarepo_model_builder.property_preprocessors import PropertyPreprocessor, process
from oarepo_model_builder.stack import ModelBuilderStack, ReplaceElement
from oarepo_model_builder.utils.camelcase import camel_case
from oarepo_model_builder.utils.deepmerge import deepmerge

from oarepo_model_builder_multilingual.datatypes import I18nDataType
from oarepo_model_builder_multilingual.utils.supported_langs import alternative_gen


def create_mapping(object, data, key):
    alternative = alternative_gen(object.settings["supported-langs"], key)
    definition = data.get("multilingual", {})

    lang = definition.get("lang-field", "lang")
    value = definition.get("value-field", "value")
    properties = data.get("properties", {})

    data = {
        key: {
            "type": "object",
            "properties": {
                lang: {"type": "keyword"},
                value: {"type": "fulltext+keyword"},
                **properties,
            },
        }
    }

    deepmerge(data, alternative)
    return data


class I18nStrPreprocessor(PropertyPreprocessor):
    @process(
        model_builder=MappingBuilder,
        path="/properties/**",
        condition=lambda current, stack: current.top.is_schema_valid,
    )
    def modify_multilang_mapping(self, data, stack: ModelBuilderStack, **kwargs):
        if stack.top.schema_element_type == "property":
            d_type = datatypes.get_datatype(
                stack.top.data,
                stack.top.key,
                self.schema.current_model,
                self.schema,
                stack,
            )
            if isinstance(d_type, I18nDataType):
                data = create_mapping(self, data, stack.top.key)
                raise ReplaceElement(data)

            elif isinstance(d_type, ArrayDataType):
                stack.push("items", stack.top.data["items"])
                d_type = datatypes.get_datatype(
                    stack.top.data,
                    stack.top.key,
                    self.schema.current_model,
                    self.schema,
                    stack,
                )
                if isinstance(d_type, I18nDataType):
                    data = create_mapping(self, data, stack[-2].key)
                    stack.pop()
                    raise ReplaceElement(data)
                stack.pop()
