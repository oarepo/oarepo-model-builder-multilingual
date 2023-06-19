from oarepo_model_builder.datatypes import (
    ArrayDataType,
    DataTypeComponent,
    ModelDataType,
    NestedDataType, datatypes,
)
from oarepo_model_builder.utils.deepmerge import deepmerge

from oarepo_model_builder_multilingual.datatypes import (
    I18nDataType,
    MultilingualDataType,
)
from oarepo_model_builder_multilingual.utils.supported_langs import alternative_gen

from .field import RegularMultilingualMappingComponent


class FieldMultilingualMappingComponent(RegularMultilingualMappingComponent):
    eligible_datatypes = [MultilingualDataType, I18nDataType]

    def create_alternative_mapping(self, datatype, *, context, **kwargs):

        if hasattr(datatype.parent, 'mapping_type') and datatype.parent.mapping_type == 'multilingual':

            return #alternative mapping already added by parent

        if not datatype.key:
            key = datatype.parent.key
            node = datatype.parent.parent
        else:
            key = datatype.key
            node = datatype.parent

        alternative = alternative_gen(
            datatype.schema.settings["supported_langs"], key
        )

        if "properties" in node.section_mapping.config:
            deepmerge(node.section_mapping.config["properties"], alternative)
        else:
            node.section_mapping.config["properties"] = alternative
