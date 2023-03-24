import json
import os
import re

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from oarepo_model_builder.fs import InMemoryFileSystem

from tests.mock_filesystem import MockFilesystem
from tests.test_helper import basic_schema

DUMMY_YAML = "test.yaml"




def test_json():
    schema = basic_schema()

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

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
            "created": {"type": "string", "format": "date"},
            "updated": {"type": "string", "format": "date"},
            "$schema": {"type": "string"},
        },
    }


def test_mapping():
    schema = basic_schema()

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = builder.filesystem.open(
        os.path.join("test", "records", "mappings", "os-v2", "test", "test-1.0.0.json")
    ).read()
    print(data)
    data = json.loads(data)
    assert data == {
    "mappings": {
        "properties": {
            "a": {
                "type": "object",
                "properties": {
                    "lang": {
                        "type": "keyword"
                    },
                    "value": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    }
                }
            },
            "a_cs": {
                "type": "text",
                "analyzer": "czech",
                "fields": {
                    "sort": {
                        "type": "icu_collation_keyword",
                        "index": False,
                        "language": "cs"
                    },
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "a_en": {
                "type": "text",
                "analyzer": "en",
                "fields": {
                    "sort": {
                        "type": "icu_collation_keyword",
                        "index": False,
                        "language": "en"
                    },
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "id": {
                "type": "keyword"
            },
            "created": {
                "type": "date"
            },
            "updated": {
                "type": "date"
            },
            "$schema": {
                "type": "keyword"
            }
        }
    }
}



def test_dumper():
    schema = basic_schema()

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = builder.filesystem.open(os.path.join("test", "records", "api.py")).read()
    assert "dumper_extensions = [MultilingualDumper()]" in data

def test_generated_schema2():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={
            "settings": {
                "supported-langs": {"cs": {}, "en": {}},
            },
            "model": {
                "properties": {
                    "a": {"type": "i18nStr", "marshmallow" : {"imports" : [{"import" :"test"}], "field-class": "FieldClassa", "arguments": ["test=cosi"]}},
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
    )

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")
    ).read()
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



from oarepo_runtime.i18n.schema import I18nStrField



from test import test





class TestSchema(ma.Schema):
    \"""TestSchema schema.\"""
    a = FieldClassa(test=cosi)
    b = I18nStrField(test=cosi, lang_field=language, value_field=val)
    """,
    )


def test_generated_schema():
    schema = basic_schema()

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = builder.filesystem.open(
        os.path.join("test", "services", "records", "schema.py")
    ).read()
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



from oarepo_runtime.i18n.schema import I18nStrField



from oarepo_runtime.i18n.schema import MultilingualField



from oarepo_runtime.ui import marshmallow as l10n



from oarepo_runtime.validation import validate_date





class TestSchema(InvenioBaseRecordSchema):
    \"""TestSchema schema.\"""
    a = MultilingualField(I18nStrField())
    created = ma_fields.String(validate=[validate_date('%Y-%m-%d')], dump_only=True)
    updated = ma_fields.String(validate=[validate_date('%Y-%m-%d')], dump_only=True)
    """,
    )


def test_sample_data():
    schema = load_model(
        "test.yaml",
        "test",
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
            "model": {
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
    )

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")
    # file = builder.filesystem.open(os.path.join("data" ,"sample_data.yaml"))
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
