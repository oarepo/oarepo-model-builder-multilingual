from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
from oarepo_model_builder.builders.mapping import MappingBuilder
from oarepo_model_builder.invenio.invenio_record_schema import (
    InvenioRecordSchemaBuilder,
)
from oarepo_model_builder.property_preprocessors import PropertyPreprocessor, process
from oarepo_model_builder.stack import ModelBuilderStack, ReplaceElement
from oarepo_model_builder.utils.deepmerge import deepmerge


def alternative_gen(supported_langs, key):
    data = {}
    for lan in supported_langs:
        alt = {
            key
            + "_"
            + lan: {
                "type": "fulltext+keyword",
            }
        }
        multilang_options = {}

        if "text" in supported_langs[lan]:
            deepmerge(multilang_options, supported_langs[lan]["text"])

        if "sort" in supported_langs[lan]:
            sort = deepmerge(
                supported_langs[lan]["sort"], {"index": False, "language": lan}
            )
            deepmerge(multilang_options, {"sort": sort})

        if "keyword" in supported_langs[lan]:
            deepmerge(
                multilang_options,
                {"fields": {"keyword": supported_langs[lan]["keyword"]}},
            )
        deepmerge(
            alt[key + "_" + lan].setdefault("mapping", {}),
            multilang_options,
            [],
        )

        data = deepmerge(data, alt)

    return data


class MultilangPreprocessor(PropertyPreprocessor):
    @process(
        model_builder=MappingBuilder,
        path="/properties/**",
        condition=lambda current, stack: current.type != "multilingual",
    )
    def modify_single_string_multilingual_opitons(
        self, data, stack: ModelBuilderStack, **kwargs
    ):
        try:
            mult_definition = data["multilingual"]
        except:
            mult_definition = None
        if not mult_definition:
            return data
        if "i18n" in mult_definition and mult_definition["i18n"] == True:
            alternative = alternative_gen(
                self.settings["supported-langs"], stack.top.key
            )
            mult_definition.pop("i18n")
            data = {stack.top.key: data, **alternative}

            raise ReplaceElement(data)

    """
    @process(
        model_builder=JSONSchemaBuilder,
        path="/properties/**",
        condition=lambda current, stack: stack.top.schema_element_type
        in ("property", "items"),
    )
    def modify_jsonschema(self, data, stack: ModelBuilderStack, **kwargs):
        datatype = datatypes.get_datatype(
            data, stack.top.key, self.schema.current_model, self.schema, stack
        )
        if not datatype:
            return data
        self.merge_with_data(data, datatype.model_schema())
        return datatype.json_schema()
    """
    @process(
        model_builder=JSONSchemaBuilder,
        path="/properties/**",
        condition=lambda current, stack: current.type == "multilingual",
    )
    def modify_multilang_schema(self, data, stack: ModelBuilderStack, **kwargs):
        data["type"] = "array"
        data["items"] = {
            "type": "object",
            "properties": {"lang": {"type": "string"}, "value": {"type": "string"}},
        }
        return data

    @process(
        model_builder=MappingBuilder,
        path="/properties/**",
        condition=lambda current, stack: current.type == "multilingual",
    )
    def modify_multilang_mapping(self, data, stack: ModelBuilderStack, **kwargs):
        alternative = alternative_gen(self.settings["supported-langs"], stack.top.key)

        data = {
            stack.top.key: {
                "type": "object",
                "properties": {
                    "lang": {"type": "keyword"},
                    "value": {"type": "fulltext"},
                },
            }
        }

        deepmerge(data, alternative)

        raise ReplaceElement(data)

    @process(
        model_builder=InvenioRecordSchemaBuilder,
        path="/properties/**",
        condition=lambda current, stack: current.type == "multilingual",
    )
    def modify_multilang_marshmallow(self, data, stack: ModelBuilderStack, **kwargs):
        data["type"] = "array"
        data["items"] = {
            "type": "object",
            "marshmallow": {
                "schema-class": self.schema.current_model.multilingual_schema_class,
                "generate": False,
            },
        }
        # deepmerge(data.setdefault('oarepo:marshmallow', {}), {
        #     'schema_class': self.settings.python.multilingual_schema_class,
        #     # 'list_nested': True
        # })

        return data
