import os
import re

from oarepo_model_builder.entrypoints import load_model, create_builder_from_entrypoints
from tests.mock_filesystem import MockFilesystem

def test_mapping():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={"oarepo:use": "invenio", "settings": {"supported_langs": ["cs"]},
                       "model": {"properties": {"a": {"type": "multilingual"}}}},
        isort=False,
        black=False,
    )

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = builder.filesystem.open(os.path.join("test", "records", "mappings", "v7", "test", "test-1.0.0.json")).read()
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
                        "type": "keyword",
                        "ignore_above": 50
                    },
                    "value": {
                        "type": "text"
                    }
                }
            },
            "a_cs": {
                "type": "text"
            },
            "id": {
                "type": "keyword",
                "ignore_above": 50
            },
            "created": {
                "type": "date"
            },
            "updated": {
                "type": "date"
            },
            "$schema": {
                "type": "keyword",
                "ignore_above": 50
            }
        }
    }
}
    """,
    )
def test_generated_schema():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={"oarepo:use": "invenio","settings": {"supported_langs" : ["cs"]}, "model": {"properties": {"a": {"type": "multilingual"}}}},
        isort=False,
        black=False,
    )

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = builder.filesystem.open(os.path.join("test", "services", "schema.py")).read()

    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
import marshmallow as ma



import marshmallow.fields as ma_fields



import marshmallow.validate as ma_valid



import oarepo_model_builder_multilingual.schema as multilingual






from multilingual import MultilingualSchema
from invenio_records_resources.services.records.schema import BaseRecordSchema as InvenioBaseRecordSchema




class TestSchema(ma.Schema, ):
    \"""TestSchema schema.\"""
    
    a = ma_fields.List(ma_fields.Nested(MultilingualSchema()))
    
    id = ma_fields.String()
    
    created = ma_fields.Date()
    
    updated = ma_fields.Date()
    
    _schema = ma_fields.String(data_key='$schema')
    """,
    )