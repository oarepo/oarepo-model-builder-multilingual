from oarepo_model_builder_multilingual.datatypes import (
    I18nDataType,
    MultilingualDataType,
)

from .field import RegularMultilingualMappingComponent, generate_alternative


class FieldMultilingualMappingComponent(RegularMultilingualMappingComponent):
    eligible_datatypes = [MultilingualDataType, I18nDataType]

    def create_alternative_mapping(self, datatype, *, context, **kwargs):
        if (
            hasattr(datatype.parent, "mapping_type")
            and datatype.parent.mapping_type == "multilingual"
        ):
            return  # alternative mapping already added by parent

        generate_alternative(datatype)
