import json
import os
import re

import yaml
from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model
from oarepo_model_builder.fs import InMemoryFileSystem

from tests.mock_filesystem import MockFilesystem
from tests.test_helper import basic_schema

DUMMY_YAML = "test.yaml"

#TODO sample
#TODO special facets
#TODO validation

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
                        "lang": {
                            "type": "string"
                        },
                        "value": {
                            "type": "string"
                        }
                    }
                },
                "type": "array",
            },
            "id": {
                "type": "string"
            },
            "created": {
                "type": "string",
                "format": "date"
            },
            "updated": {
                "type": "string",
                "format": "date"
            },
            "$schema": {
                "type": "string"
            }
        }
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
  "mappings":{
    "properties":{
      "a":{
        "type":"object",
        "properties":{
          "lang":{
            "type":"keyword"
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
      "a_cs":{
        "type":"text",
        "analyzer":"czech",
        "sort":{
          "type":"icu_collation_keyword",
          "index":False,
          "language":"cs"
        },
        "fields":{
          "keyword":{
            "type":"keyword"
          }
        }
      },
      "a_en":{
        "type":"text",
        "analyzer":"en",
        "sort":{
          "type":"icu_collation_keyword",
          "index":False,
          "language":"en"
        },
        "fields":{
          "keyword":{
            "type":"keyword"
          }
        }
      },
      "id":{
        "type":"keyword"
      },
      "created":{
        "type":"date"
      },
      "updated":{
        "type":"date"
      },
      "$schema":{
        "type":"keyword"
      }
    }
  }
}


# Multilingual dumper was moved to the oarepo-runtime library
# todo import dumper!
def test_dumper():
    schema = basic_schema()

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = builder.filesystem.open(os.path.join("test", "records", "api.py")).read()
    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
from invenio_records.systemfields import ConstantField
from invenio_records_resources.records.systemfields import IndexField,

from invenio_records_resources.records.systemfields.pid import PIDField, PIDFieldContext
from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2


from invenio_records_resources.records.api import Record

from test.records.models import TestMetadata
from test.records.dumper import TestDumper
from test.records.multilingual_dumper import MultilingualDumper

class TestRecord(Record ):
    model_cls = TestMetadata

    schema = ConstantField("$schema", "http://localhost/schemas/test-1.0.0.json")


    index = IndexField("test-test-1.0.0")


    pid = PIDField(
        create=True,
        provider=RecordIdProviderV2,
        context_cls = PIDFieldContext
    )

    dumper_extensions = [MultilingualDumper()]
    dumper = TestDumper(extensions=dumper_extensions)

    """,
    )


def test_generated_schema():
    schema = basic_schema()

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



from oarepo_runtime.ui import marshmallow as l10n



from oarepo_runtime.validation import validate_date





class AItemSchema(ma.Schema):
    \"""AItemSchema schema.\"""
    lang = ma_fields.String()
    value = ma_fields.String()



class TestSchema(InvenioBaseRecordSchema):
    \"""TestSchema schema.\"""
    a = ma_fields.List(ma_fields.Nested(lambda: AItemSchema()))
    created = ma_fields.String(validate=[validate_date('%Y-%m-%d')], dump_only=True)
    updated = ma_fields.String(validate=[validate_date('%Y-%m-%d')], dump_only=True)
    """,
    )


# # TODO validace jazyku do oarepo-runtime
# def test_multilingual_schema():
#     schema = basic_schema()
#
#     filesystem = MockFilesystem()
#     builder = create_builder_from_entrypoints(filesystem=filesystem)
#
#     builder.build(schema, "")
#
#     data = builder.filesystem.open(os.path.join("test", "services", "records", "multilingual_schema.py")).read()
#     print(data)
#
#     assert re.sub(r"\s", "", data) == re.sub(
#         r"\s",
#         "",
#         """
# import langcodes
# from marshmallow import Schema, fields, ValidationError, validates
#
# \"""
# Marshmallow schema for multilingual strings. Consider moving this file to a library, not generating
# it for each project.
# \"""
#
#
# class MultilingualSchema(Schema):
#     lang = fields.String(required=True)
#     value = fields.String(required=True)
#
#     @validates("lang")
#     def validate_lang(self, value):
#         if value != '_' and not langcodes.Language.get(value).is_valid():
#             raise ValidationError("Invalid language code")
#
#     """,
#     )


# def test_sample_data():
#     schema = load_model(
#         "test.yaml",
#         "test",
#         model_content={
#
#             "settings": {
#                 "supported-langs": {
#                     "cs": {
#                         "text": {
#                             "analyzer": "czech",
#                         },
#                         "sort": {"type": "icu_collation_keyword"},
#                         "keyword": {"test": "test"},
#                     },
#                     "en": {
#                         "text": {"analyzer": "czech"},
#                         "sort": {"type": "icu_collation_keyword"},
#                     },
#                 }
#             },
#             "model": {"use": "invenio", "sample": {"count": 1}, "properties": {"a": {"type": "multilingual"}}},
#
#         },
#         isort=False,
#         black=False,
#     )
#
#     filesystem = MockFilesystem()
#     builder = create_builder_from_entrypoints(filesystem=filesystem)
#
#     builder.build(schema, "")
#     # file = builder.filesystem.open(os.path.join("data" ,"sample_data.yaml"))
#     data_yaml = builder.filesystem.open(os.path.join("data", "sample_data.yaml")).read()
#     import yaml
#     yaml_docs = data_yaml.split('---')
#     for doc in yaml_docs:
#         if doc.strip():
#             data = yaml.safe_load(doc)
#             print(data)
#             assert isinstance(data["a"], list)
#             assert len(data["a"]) == 2
#             assert set(x["lang"] for x in data["a"]) == {"cs", "en"}
