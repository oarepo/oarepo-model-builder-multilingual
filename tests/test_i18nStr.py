import json
import os
import re

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model

from oarepo_model_builder.fs import InMemoryFileSystem

def test_generated_jsonschema():
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
                    "a": {"type": "i18nStr"},
                    "b": {
                        "type": "i18nStr",
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
        os.path.join("test", "records", "jsonschemas", "test-1.0.0.json")
    ).read()
    print(data)
    data = json.loads(data)
    assert data == {
        "type": "object",
        "properties": {
            "a": {
                "type": "object",
                "properties": {"lang": {"type": "string"}, "value": {"type": "string"}},
            },
            "b": {
                "type": "object",
                "properties": {
                    "language": {"type": "string"},
                    "val": {"type": "string"},
                },
            },
        },
    }


def test_generated_mapping():
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
                    "a": {"type": "i18nStr"},
                    "b": {
                        "type": "i18nStr",
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
                    "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
                },
                "a_en": {
                    "type": "text",
                    "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
                },
                "b": {
                    "type": "nested",
                    "properties": {
                        "language": {"type": "keyword", "ignore_above": 256},
                        "val": {
                            "type": "text",
                            "fields": {
                                "keyword": {"type": "keyword", "ignore_above": 256}
                            },
                        },
                    },
                },
                "b_cs": {
                    "type": "text",
                    "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
                },
                "b_en": {
                    "type": "text",
                    "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
                },
            }
        }
    }


def test_generated_schema():
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
                    "a": {"type": "i18nStr"},
                    "b": {
                        "type": "i18nStr",
                        "multilingual": {
                            "lang-field": "language",
                            "value-field": "val",
                        },
                    },
                    "c": {"properties": {"d": "keyword"}},
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
from marshmallow import fields as ma_fields

from oarepo_runtime.services.schema.i18n import I18nStrField

from marshmallow import Schema

from oarepo_runtime.services.schema.marshmallow import DictOnlySchema

class TestSchema(Schema):

    class Meta:
        unknown = ma.RAISE


    a = I18nStrField()

    b = I18nStrField(lang_field=language, value_field=val)
    
    c = ma_fields.Nested(lambda: CSchema())

class CSchema(DictOnlySchema):

    class Meta:
        unknown = ma.RAISE


    d = ma_fields.String()

    """,
    )


def test_mapping():
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
                            "f": {"type": "array", "items": {"type": "i18nStr"}},
                            "d": {"type": "array", "items": {"type": "multilingual"}},
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
        os.path.join("test", "records", "mappings", "os-v2", "test", "test-1.0.0.json")
    ).read()
    print(data)
