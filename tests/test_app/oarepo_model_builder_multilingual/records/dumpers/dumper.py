from oarepo_runtime.records.dumpers import SearchDumper

from oarepo_model_builder_multilingual.records.dumpers.edtf import (
    OarepoModelBuilderMultilingualEDTFIntervalDumperExt,
)


class OarepoModelBuilderMultilingualDumper(SearchDumper):
    """OarepoModelBuilderMultilingualRecord opensearch dumper."""

    extensions = [
        OarepoModelBuilderMultilingualEDTFIntervalDumperExt(),
        MultilingualSearchDumper(),
    ]
