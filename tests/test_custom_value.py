import json
import os
import re

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from oarepo_model_builder.fs import InMemoryFileSystem

from tests.mock_filesystem import MockFilesystem

DUMMY_YAML = "test.yaml"

def base_schema():
    return load_model(
        "test.yaml",
        model_content={
            "settings": {
                "supported-langs": {"cs": {}, "en": {}},
            },
            "record": {
                "module": {"qualified": "test"},
                "properties": {
                    "a": {"type": "i18nStr", "multilingual": {"value-type": "integer"}},
                    "b": {
                        "type": "i18nStr",
                        "multilingual": {
                            "lang-name": "language",
                            "value-name": "val",
                            "value-type": "integer"
                        },
                    }
                },
            },
        },
        isort=False,
        black=False,
        autoflake=False,
    )

def test_json():
    schema = base_schema()

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "record", ["record"], "")

    data = builder.filesystem.open(
        os.path.join("test", "records", "jsonschemas", "test-1.0.0.json")
    ).read()
    print(data)
    data = json.loads(data)
    assert data == {
        "type": "object",
        "properties": {
            "a": {
                "type": "object",
                "properties": {
                    "lang": {
                        "type": "string"
                    },
                    "value": {
                        "type": "integer"
                    }
                }
            },
            "b": {
                "type": "object",
                "properties": {
                    "language": {
                        "type": "string"
                    },
                    "val": {
                        "type": "integer"
                    }
                }
            }
        }
    }


def test_mapping():
    schema = base_schema()

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "record", ["record"], "")

    data = builder.filesystem.open(
        os.path.join("test", "records", "mappings", "os-v2", "test", "test-1.0.0.json")
    ).read()
    print(data)
    data = json.loads(data)
    assert data == {
        "mappings": {
            "properties": {
                "a_cs": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "a_en": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "b_cs": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "b_en": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "a": {
                    "type": "nested",
                    "properties": {
                        "lang": {
                            "ignore_above": 256,
                            "type": "keyword"
                        },
                        "value": {
                            "type": "integer"
                        }
                    }
                },
                "b": {
                    "type": "nested",
                    "properties": {
                        "language": {
                            "ignore_above": 256,
                            "type": "keyword"
                        },
                        "val": {
                            "type": "integer"
                        }
                    }
                }
            }
        }
    }


def test_dumper():
    schema = base_schema()

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "record", ["record"], "")

    data = builder.filesystem.open(
        os.path.join("test", "records", "dumpers", "dumper.py")
    ).read()
    print(data)
    data = str(data)
    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
from oarepo_runtime.records.dumpers import SearchDumper

from test.records.dumpers.multilingual import MultilingualSearchDumperExt

from test.records.dumpers.edtf import TestEDTFIntervalDumperExt


class TestDumper(SearchDumper):
    \"""TestRecord opensearch dumper.\"""
    extensions =  [ MultilingualSearchDumperExt(), TestEDTFIntervalDumperExt() ]
    """,
    )


def test_dumper_file():
    schema = base_schema()

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "record", ["record"], "")

    data = builder.filesystem.open(
        os.path.join("test", "records", "dumpers", "multilingual.py")
    ).read()
    print(data)
    assert "/a" in re.sub(r"\s", "", data)
    assert "/b" in re.sub(r"\s", "", data)


def test_generated_schema2():
    schema = load_model(
        "test.yaml",
        model_content={
            "settings": {
                "supported-langs": {"cs": {}, "en": {}},
            },
            "record": {
                "module": {"qualified": "test"},
                "properties": {
                    "a": {
                        "type": "i18nStr",
                        "marshmallow": {
                            "field-class": "test.FieldClassa",
                            "arguments": ["test=cosi"],
                        },
                    },
                    "b": {
                        "type": "i18nStr",
                        "marshmallow": {"arguments": ["test=cosi"]},
                        "multilingual": {
                            "lang-name": "language",
                            "value-name": "val",
                            "value-field": "marshmallow.fields.String"
                        },
                    },
                },
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
        os.path.join("test", "services", "records", "schema.py")
    ).read()
    print(data)

    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
import marshmallow as ma

from oarepo_runtime.services.schema.i18n import I18nStrField
from test import FieldClassa

from marshmallow import Schema


class TestSchema(Schema):

    class Meta:
        unknown = ma.RAISE


    a = FieldClassa(test=cosi)

    b = I18nStrField(test=cosi, lang_name=language, value_field=marshmallow.fields.String, value_name=val)

    """,
    )

