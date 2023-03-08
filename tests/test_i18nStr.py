import os
import re

import yaml
from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model

from tests.mock_filesystem import MockFilesystem


def test_generated_jsonschema():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={
            "settings": {
                "supported-langs": {"cs": {}, "en": {}},
            },
            "model": {
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
    )

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = builder.filesystem.open(
        os.path.join("test", "records", "jsonschemas", "test-1.0.0.json")
    ).read()
    print(data)
    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
{
    "type": "object",
    "properties": {
        "a": {
            "type": "object",
            "properties": {
                "lang": {
                    "type": "string"
                },
                "value": {
                    "type": "string"
                }
            },
            "required": [
                "lang",
                "value"
            ]
        },
        "b": {
            "type": "object",
            "properties": {
                "language": {
                    "type": "string"
                },
                "val": {
                    "type": "string"
                }
            },
            "required": [
                "language",
                "val"
            ]
        }
    }
}


    """,
    )

def test_generated_mapping():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={
            "settings": {
                "supported-langs": {"cs": {}, "en": {}},
            },
            "model": {
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
    )

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = builder.filesystem.open(
        os.path.join("test", "records", "mappings", "os-v2", "test", "test-1.0.0.json")
    ).read()
    print(data)
    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
{
    "mappings": {
        "properties": {
            "a": {
                "type": "object",
                "properties": {
                    "lang": {
                        "type": "keyword"
                    },
                    "value": {
                        "type": "text"
                    }
                }
            },
            "a_cs": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "a_en": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "b": {
                "type": "object",
                "properties": {
                    "language": {
                        "type": "keyword"
                    },
                    "val": {
                        "type": "text"
                    }
                }
            },
            "b_cs": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "b_en": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            }
        }
    }
}


    """,
    )


# todo - validation will be added after model-builder release
#todo validace language kde??
def test_generated_schema():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={
            "settings": {
                "supported-langs": {"cs": {}, "en": {}},
            },
            "model": {
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
    )

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = builder.filesystem.open(os.path.join("test", "services", "records", "schema.py")).read()
    print(data)
    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
from invenio_records_resources.services.records.schema import BaseRecordSchema as InvenioBaseRecordSchema
from marshmallow import ValidationError
from marshmallow import validate as ma_validate
import marshmallow as ma
from marshmallow import fields as ma_fields
from marshmallow_utils import fields as mu_fields
from marshmallow_utils import schemas as mu_schemas



from test.services.records.i18nStr_schema import i18nStrSchema





class BSchema(ma.Schema):
    \"""BSchema schema.\"""
    language = ma_fields.String()
    val = ma_fields.String()



class TestSchema(ma.Schema):
    \"""TestSchema schema.\"""
    a = ma_fields.Nested(lambda: i18nStrSchema())
    b = ma_fields.Nested(lambda: BSchema())
    """,
    )


# todo - validation will be added after model-builder release
def test_generated_schema_use_i18n():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={
            "settings": {"supported-langs": {"cs": {}, "en": {}}},
            "model": {
                "properties": {
                    "a": {
                        "use": "i18n",
                        "properties": {
                            "navic": {
                                "type": "object",
                                "properties": {"kxh": {"type": "keyword"}},
                            }
                        },
                    }
                },
            },
        },
        isort=False,
        black=False,
    )

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = builder.filesystem.open(os.path.join("test", "services", "schema.py")).read()
    print(data)
    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
import marshmallow as ma
import marshmallow.fields as ma_fields
import marshmallow.validate as ma_valid
from invenio_records_resources.services.records.schema import BaseRecordSchema as InvenioBaseRecordSchema
class NavicSchema(ma.Schema, ):
    \"""NavicSchema schema.\"""
    
    kxh = ma_fields.String()
    
class ASchema(ma.Schema, ):
    \"""ASchema schema.\"""
    
    lang = ma_fields.String()
    
    value = ma_fields.String()
    
    navic = ma_fields.Nested(lambda: NavicSchema())

class TestSchema(ma.Schema, ):
    \"""TestSchema schema.\"""
    
    a = ma_fields.Nested(lambda: ASchema())
    """,
    )


def test_mapping():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={
            "settings": {"supported-langs": {"cs": {}, "en": {}}},
            "model": {
                "properties": {
                    "a": {"type": "fulltext", "multilingual": {"i18n": True}}
                }
            },
        },
        isort=False,
        black=False,
    )

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = builder.filesystem.open(
        os.path.join("test", "records", "mappings", "os-v2", "test", "test-1.0.0.json")
    ).read()
    print(data)
    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
{"mappings":{"properties":{"a":{"type":"text"},
"a_cs":{"type":"text","fields":{"keyword":{"type":"keyword"}}},
"a_en":{"type":"text","fields":{"keyword":{"type":"keyword"}}}}}}
    """,
    )
