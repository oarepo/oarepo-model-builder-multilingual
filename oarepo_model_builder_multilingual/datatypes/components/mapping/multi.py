from oarepo_model_builder.datatypes import (
    ArrayDataType,
    DataTypeComponent,
    ModelDataType,
    NestedDataType,
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

    def after_model_prepare(self, datatype, *, context, **kwargs):
        alternative = alternative_gen(
            datatype.schema.settings["supported_langs"], datatype.key
        )
        if "properties" in datatype.parent.section_mapping.config:
            deepmerge(datatype.parent.section_mapping.config["properties"], alternative)
        else:
            datatype.parent.section_mapping.config["properties"] = alternative
