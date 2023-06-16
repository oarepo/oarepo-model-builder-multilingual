
from oarepo_model_builder.datatypes import (
    DataTypeComponent,
    datatypes,
)


class RegularMultilingualMappingComponent(DataTypeComponent):
    eligible_datatypes = []

    def after_model_prepare(self, datatype, *, context, **kwargs):
        for node in datatype.deep_iter():
            datatypes.call_components(
                node, "create_alternative_mapping", context=context
            )

