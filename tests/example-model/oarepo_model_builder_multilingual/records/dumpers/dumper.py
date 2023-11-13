from oarepo_runtime.records.dumpers import SearchDumper

from oarepo_model_builder_multilingual.records.dumpers.edtf import (
    OarepoModelBuilderMultilingualEDTFIntervalDumperExt,
)
from oarepo_model_builder_multilingual.records.dumpers.multilingual import (
    MultilingualSearchDumperExt,
)


class OarepoModelBuilderMultilingualDumper(SearchDumper):
    """OarepoModelBuilderMultilingualRecord opensearch dumper."""

    extensions = [
        OarepoModelBuilderMultilingualEDTFIntervalDumperExt(),
        MultilingualSearchDumperExt(),
    ]
