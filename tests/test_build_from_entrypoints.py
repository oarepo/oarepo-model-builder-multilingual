import json
import os
import re

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from oarepo_model_builder.fs import InMemoryFileSystem

from tests.test_helper import basic_schema

DUMMY_YAML = "test.yaml"


def test_json():
    schema = basic_schema()

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
                "items": {
                    "type": "object",
                    "properties": {
                        "lang": {"type": "string"},
                        "value": {"type": "string"},
                    },
                },
                "type": "array",
            },
            "id": {"type": "string"},
            "pid": {
                "properties": {
                    "obj_type": {"type": "string"},
                    "pid_type": {"type": "string"},
                    "pk": {"type": "integer"},
                    "status": {"type": "string"},
                },
                "type": "object",
            },
            "created": {"type": "string", "format": "date-time"},
            "updated": {"type": "string", "format": "date-time"},
            "$schema": {"type": "string"},
        },
    }


def test_mapping():
    schema = basic_schema()

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
                "a": {
                    "type": "nested",
                    "properties": {
                        "lang": {"type": "keyword", "ignore_above": 256},
                        "value": {
                            "type": "text",
                            "fields": {
                                "keyword": {"type": "keyword", "ignore_above": 256}
                            },
                        },
                    },
                },
                "a_cs": {
                    "type": "text",
                    "analyzer": "czech",
                    "fields": {
                        "sort": {
                            "type": "icu_collation_keyword",
                            "index": False,
                            "language": "cs",
                        },
                        "keyword": {"type": "keyword", "ignore_above": 256},
                    },
                },
                "a_en": {
                    "type": "text",
                    "analyzer": "en",
                    "fields": {
                        "sort": {
                            "type": "icu_collation_keyword",
                            "index": False,
                            "language": "en",
                        },
                        "keyword": {"type": "keyword", "ignore_above": 256},
                    },
                },
                "id": {"type": "keyword", "ignore_above": 1024},
                "pid": {
                    "properties": {
                        "obj_type": {"ignore_above": 1024, "type": "keyword"},
                        "pid_type": {"ignore_above": 1024, "type": "keyword"},
                        "pk": {"type": "integer"},
                        "status": {"ignore_above": 1024, "type": "keyword"},
                    },
                    "type": "object",
                },
                "created": {
                    "format": "strict_date_time||strict_date_time_no_millis||basic_date_time||basic_date_time_no_millis||basic_date||strict_date||strict_date_hour_minute_second||strict_date_hour_minute_second_fraction",
                    "type": "date",
                },
                "updated": {
                    "format": "strict_date_time||strict_date_time_no_millis||basic_date_time||basic_date_time_no_millis||basic_date||strict_date||strict_date_hour_minute_second||strict_date_hour_minute_second_fraction",
                    "type": "date",
                },
                "$schema": {"type": "keyword", "ignore_above": 1024},
            }
        }
    }


def test_mapping2():
    schema = load_model(
        "test.yaml",
        model_content={

            "settings": {
                "i18n-languages": ["cs", "en"],
                "supported-langs": {
                    "cs": {
                        "keyword": {"type": "keyword", "ignore_above": 256},
                        "text": {"analyzer": "czech"},
                    },
                    "en": {},
                },
            },
            "record": {
                "module": {"qualified": "test"},
                "properties": {
                    "b[]": {"properties": {"c": "multilingual"}},
                    "notes[]": "fulltext",
                    "keywords[]": "multilingual",
                    "abstract": "multilingual",
                    "methods": "multilingual",
                    "technicalInfo": "multilingual",
                },
            },
        },
        isort=False,
        black=False,
        autoflake=False,
    )

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "record", ["record"], "")

    data = builder.filesystem.open(
        os.path.join("test", "records", "mappings", "os-v2", "test", "test-1.0.0.json")
    ).read()
    print(data)
    # data = builder.filesystem.open(
    #     os.path.join("test", "services", "records", "facets.py")
    # ).read()
    #
    # print(data)


def test_dumper():
    schema = basic_schema()

    filesystem = InMemoryFileSystem()
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
    schema = load_model(
        "test.yaml",
        model_content={

            "settings": {
                "i18n-languages": ["cs", "en"],
                "supported-langs": {"cs": {}, "en": {}},
            },
            "record": {
                "module": {"qualified": "test"},
                "properties": {
                    "h": "keyword",
                    "a": {"type": "i18nStr"},
                    "b": {"type": "multilingual"},
                    "jej": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {"kch": {"type": "multilingual"}},
                        },
                    },
                    "c": {
                        "type": "object",
                        "properties": {
                            "d": {"type": "array", "items": {"type": "multilingual"}},
                            "f": {"type": "array", "items": {"type": "i18nStr"}},
                        },
                    },
                },
            },
        },
        isort=False,
        black=False,
        autoflake=False,
    )

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "record", ["record"], "")

    data = builder.filesystem.open(
        os.path.join("test", "records", "dumpers", "multilingual.py")
    ).read()
    print(data)
    assert "/a" in re.sub(r"\s", "", data)
    assert "/b" in re.sub(r"\s", "", data)
    assert "/c/d" in re.sub(r"\s", "", data)
    assert "/c/f" in re.sub(r"\s", "", data)
    assert "/jej/kch" in re.sub(r"\s", "", data)


def test_generated_schema2():
    schema = load_model(
        "test.yaml",
        model_content={

            "settings": {
                "i18n-languages": ["cs", "en"],
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
                            "lang-field": "language",
                            "value-field": "val",
                        },
                    },
                },
            },
        },
        isort=False,
        black=False,
        autoflake=False,
    )

    filesystem = InMemoryFileSystem()
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

    b = I18nStrField(test=cosi, lang_field=language, value_field=val)

    """,
    )


def test_generated_schema():
    schema = load_model(
        DUMMY_YAML,
        model_content={

            "settings": {
                "i18n-languages": ["cs", "en"],
                "supported-langs": {
                    "cs": {
                        "text": {
                            "analyzer": "czech",
                        },
                        "sort": {"type": "icu_collation_keyword"},
                    },
                    "en": {
                        "text": {"analyzer": "en"},
                        "sort": {"type": "icu_collation_keyword"},
                    },
                }
            },
            "record": {
                "module": {"qualified": "test"},
                "properties": {"a": {"type": "multilingual"}},
            },
        },
        isort=False,
        black=False,
        autoflake=False,
    )

    filesystem = InMemoryFileSystem()
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
from oarepo_runtime.services.schema.i18n import MultilingualField

from marshmallow import Schema

class TestSchema(Schema):

    class Meta:
        unknown = ma.RAISE


    a = MultilingualField(I18nStrField())
    """,
    )


def test_sample_data():
    schema = load_model(
        "test.yaml",
        model_content={

            "settings": {
                "i18n-languages": ["cs", "en"],
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
                "module": {"qualified": "test"},
                "use": "invenio",
                "sample": {"count": 1},
                "properties": {
                    "a": {"type": "multilingual"},
                    "b": {"type": "i18nStr"},
                    "c": {
                        "type": "object",
                        "properties": {"d": "multilingual", "e": "keyword"},
                    },
                },
            },
        },
        isort=False,
        black=False,
        autoflake=False,
    )

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "record", ["record"], "")
    data_yaml = builder.filesystem.open(os.path.join("data", "sample_data.yaml")).read()
    import yaml

    yaml_docs = data_yaml.split("---")
    for doc in yaml_docs:
        if doc.strip():
            data = yaml.safe_load(doc)
            print(data)
            assert isinstance(data["a"], list)
            for i18n in data["a"]:
                assert i18n["lang"] in ("cs", "en")

            assert isinstance(data["b"], dict)
            assert data["b"]["lang"] in ("cs", "en")


def test_non_i18n_mapping():
    schema = load_model(
        "test.yaml",
        model_content={

            "settings": {"i18n-languages": ["cs", "en"],
                         "supported-langs": {"cs": {}, "en": {}}},
            "record": {
                "module": {"qualified": "test"},
                "properties": {
                    "a": {"type": "fulltext", "multilingual": {"i18n": True}},
                    "b[]": {"type": "keyword", "multilingual": {"i18n": True}},
                    "c": {
                        "properties": {
                            "d": {"type": "keyword", "multilingual": {"i18n": True}}
                        }
                    },
                },
            },
        },
        isort=False,
        black=False,
        autoflake=False,
    )

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
                    "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
                },
                "a_en": {
                    "type": "text",
                    "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
                },
                "b_cs": {
                    "type": "text",
                    "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
                },
                "b_en": {
                    "type": "text",
                    "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
                },
                "a": {"type": "text"},
                "b": {"type": "keyword", "ignore_above": 1024},
                "c": {
                    "type": "object",
                    "properties": {
                        "d_cs": {
                            "type": "text",
                            "fields": {
                                "keyword": {"type": "keyword", "ignore_above": 256}
                            },
                        },
                        "d_en": {
                            "type": "text",
                            "fields": {
                                "keyword": {"type": "keyword", "ignore_above": 256}
                            },
                        },
                        "d": {"type": "keyword", "ignore_above": 1024},
                    },
                },
            }
        }
    }
