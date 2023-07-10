from oarepo_model_builder.datatypes import DataTypeComponent, datatypes
from oarepo_model_builder.utils.deepmerge import deepmerge

from oarepo_model_builder_multilingual.utils.supported_langs import alternative_gen


def generate_alternative(datatype):
    if not datatype.key:
        key = datatype.parent.key
        node = datatype.parent.parent
    else:
        key = datatype.key
        node = datatype.parent
    alternative = alternative_gen(datatype.schema.settings["supported-langs"], key)
    if "properties" in node.section_mapping.config:
        deepmerge(node.section_mapping.config["properties"], alternative)
    else:
        node.section_mapping.config["properties"] = alternative


class RegularMultilingualMappingComponent(DataTypeComponent):
    eligible_datatypes = []

    def create_alternative_mapping(self, datatype, *, context, **kwargs):
        if (
            "i18n" in datatype.section_multilingual.config
            and datatype.section_multilingual.config["i18n"]
        ):
            generate_alternative(datatype)

    def after_model_prepare(self, datatype, *, context, **kwargs):
        for node in datatype.deep_iter():
            datatypes.call_components(
                node, "create_alternative_mapping", context=context
            )
