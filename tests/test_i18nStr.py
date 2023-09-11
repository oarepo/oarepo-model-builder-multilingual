import json
import os
import re

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model

from tests.mock_filesystem import MockFilesystem


def test_generated_jsonschema():
    schema = load_model(
        "test.yaml",
        model_content={
            "settings": {
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

    filesystem = MockFilesystem()
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

    filesystem = MockFilesystem()
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
                            "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
                        },
                    },
                },
                "a_cs": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
                "a_en": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
                "b": {
                    "type": "nested",
                    "properties": {
                        "language": {"type": "keyword", "ignore_above": 256},
                        "val": {
                            "type": "text",
                            "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
                        },
                    },
                },
                "b_cs": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
                "b_en": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            }
        }
    }


def test_generated_schema():
    schema = load_model(
        "test.yaml",
        model_content={
            "settings": {
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
from marshmallow import ValidationError
from marshmallow import validate as ma_validate
import marshmallow as ma
from marshmallow_utils import fields as mu_fields
from marshmallow_utils import schemas as mu_schemas

from oarepo_runtime.i18n.schema import I18nStrField


class TestSchema(ma.Schema):

    class Meta:
        unknown = ma.RAISE


    a = I18nStrField()

    b = I18nStrField(lang_field=language, value_field=val)
    
    c = ma.fields.Nested(lambda: CSchema())

class CSchema(ma.Schema):

    class Meta:
        unknown = ma.RAISE


    d = ma.fields.String()

    """,
    )


def test_mapping():
    schema = load_model(
        "test.yaml",
        model_content={
            "settings": {
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

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "record", ["record"], "")

    data = builder.filesystem.open(
        os.path.join("test", "records", "mappings", "os-v2", "test", "test-1.0.0.json")
    ).read()
    print(data)
