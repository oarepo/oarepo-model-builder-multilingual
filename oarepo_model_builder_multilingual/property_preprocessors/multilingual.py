from oarepo_model_builder.builders.mapping import MappingBuilder
from oarepo_model_builder.invenio.invenio_record_schema import (
    InvenioRecordSchemaBuilder,
)
from oarepo_model_builder.property_preprocessors import PropertyPreprocessor, process
from oarepo_model_builder.stack import ModelBuilderStack, ReplaceElement

from oarepo_model_builder_multilingual.utils.supported_langs import alternative_gen


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
