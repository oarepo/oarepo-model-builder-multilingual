
from oarepo_model_builder.datatypes import (
    DataTypeComponent,
    datatypes,
)


class RegularMultilingualMappingComponent(DataTypeComponent):
    eligible_datatypes = []

    def after_model_prepare(self, datatype, *, context, **kwargs):
        for c in datatype.children:
            datatypes.call_components(
                datatype.children[c], "after_model_prepare", context=context
            )

