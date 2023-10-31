import os
import re

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model

from tests.mock_filesystem import MockFilesystem


def test_dumper():
    schema = load_model(
        "test.yaml",
        model_content={
            "settings": {
                "supported-langs": {
                    "cs": {
                        "text": {
                            "analyzer": "czech",
                        },
                        "sort": {"type": "icu_collation_keyword"},
                        "keyword": {"test": "test"},
                    },
                    "en": {
                        "text": {"analyzer": "czech"},
                        "sort": {"type": "icu_collation_keyword"},
                    },
                }
            },
            "record": {
                "use": "invenio",
                "module": {"qualified": "test"},
                "properties": {"a": {"type": "multilingual"}},
            },
        },
        isort=False,
        black=False,
        autoflake=False,
    )

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "record", ["record"], "")

    data = builder.filesystem.open(
        os.path.join("test", "records", "dumpers", "dumper.py")
    ).read()

    print(data)
    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
from oarepo_runtime.records.dumpers import SearchDumper

from test.records.multilingual_dumper import MultilingualSearchDumperExt

from test.records.dumpers.edtf import TestEDTFIntervalDumperExt


class TestDumper(SearchDumper):
    \"""TestRecord opensearch dumper.\"""
    extensions =  [ MultilingualSearchDumperExt(), TestEDTFIntervalDumperExt() ]
    """,
    )
