import os
import re

from oarepo_model_builder.entrypoints import load_model, create_builder_from_entrypoints
from tests.mock_filesystem import MockFilesystem

import yaml

from tests.test_helper import basic_schema


def test_mapping():
    schema = basic_schema()

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = builder.filesystem.open(os.path.join("test", "records", "mappings", "os-v2", "test", "test-1.0.0.json")).read()
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
                "analyzer": "czech",
                "sort": {
                    "type": "icu_collation_keyword",
                    "index": false,
                    "language": "cs"
                },
                "fields": {
                    "keyword": {
                        "test": "test",
                        "type": "keyword"
                    }
                }
            },
            "a_en": {
                "type": "text",
                "analyzer": "en",
                "sort": {
                    "type": "icu_collation_keyword",
                    "index": false,
                    "language": "en"
                },
                "fields": {
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
    """,
    )

def test_dumper():
    schema = basic_schema()

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    # data = builder.filesystem.open(os.path.join("test", "records", "multilingual_dumper.py")).read()
    # print(data)
    data = builder.filesystem.open(os.path.join("test", "records", "api.py")).read()

def test_generated_schema():
    schema = basic_schema()

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = builder.filesystem.open(os.path.join("test", "services","records", "schema.py")).read()
    data_2 = builder.filesystem.open(os.path.join("test", "services", "records", "multilingual_schema.py")).read()
    print(data)
    print(data_2)

    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
from invenio_records_resources.services.records.schema import BaseRecordSchema as InvenioBaseRecordSchema
from marshmallow import ValidationError
from marshmallow import validates as ma_validates
import marshmallow as ma
from marshmallow import fields as ma_fields
from marshmallow_utils import fields as mu_fields
from marshmallow_utils import schemas as mu_schemas



from test.services.records.multilingual_schema import MultilingualSchema





class TestSchema(InvenioBaseRecordSchema):
    \"""TestSchema schema.\"""
    a = ma_fields.List(ma_fields.Nested(lambda: MultilingualSchema()))
    created = mu_fields.ISODateString(dump_only=True)
    updated = mu_fields.ISODateString(dump_only=True)
    """,
    )
def test_generated_ml_schema():
    schema = basic_schema()

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = builder.filesystem.open(os.path.join("test", "services", "records", "multilingual_schema.py")).read()
    print(data)

    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
import langcodes
from marshmallow import Schema, fields, ValidationError, validates

\"""
Marshmallow schema for multilingual strings. Consider moving this file to a library, not generating
it for each project.
\"""


class MultilingualSchema(Schema):
    lang = fields.String(required=True)
    value = fields.String(required=True)

    @validates("lang")
    def validate_lang(self, value):
        if value != '_' and not langcodes.Language.get(value).is_valid():
            raise ValidationError("Invalid language code")
    """,
    )
def test_sample_data():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={"oarepo:use": "invenio", "settings": {"supported-langs": {
            'cs': {
                'text': {
                    'analyzer': 'czech',
                },
                'sort': {
                    'type': 'icu_collation_keyword'
                },
                'keyword': {
                    'test': 'test'
                }
            },
            'en': {
                'text': {
                    'analyzer': 'czech'
                },
                'sort': {
                    'type': 'icu_collation_keyword'
                }
            }
        }},
                       "model": {"properties": {"a": {"type": "multilingual"}}},
                       "oarepo:sample": {"count": 1}},
        isort=False,
        black=False,
    )

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = yaml.full_load(builder.filesystem.open(os.path.join("scripts", "sample_data.yaml")).read())

    assert isinstance(data['a'], list)
    assert len(data['a']) == 2
    assert set(x['lang'] for x in data['a']) == {'cs', 'en'}

def test_search_options():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={"oarepo:use": "invenio", "settings": {"supported-langs": {
            'cs': {
                'text': {
                    'analyzer': 'czech',
                },
                'sort': {
                    'type': 'icu_collation_keyword'
                },
                'keyword': {
                    'test': 'test'
                }
            },
            'en': {
                'text': {
                    'analyzer': 'czech'
                },
                'sort': {
                    'type': 'icu_collation_keyword'
                }
            }
        }},
                       "model": {"properties": {"a": {"type": "multilingual", "oarepo:sortable":{}}}}},
        isort=False,
        black=False,
    )

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = builder.filesystem.open(os.path.join("test", "services","records", "search.py")).read()
    print(data)
    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
from invenio_records_resources.services import SearchOptions as InvenioSearchOptions
from . import facets

def _(x):
    \"""Identity function for string extraction.\"""
    return x



class TestSearchOptions(InvenioSearchOptions):
    \"""TestRecord search options.\"""

    facets = {


    'a': facets.a,



    '_id': facets._id,



    'created': facets.created,



    'updated': facets.updated,



    '_schema': facets._schema,


    }
    sort_options = {
        
        **InvenioSearchOptions.sort_options,
        


    'a': {'fields': ['a']},"bestmatch": dict(
                title=_('Best match'),
                fields=['_score'],  # ES defaults to desc on `_score` field
            ),
            "newest": dict(
                title=_('Newest'),
                fields=['-created'],
            ),
            "oldest": dict(
                title=_('Oldest'),
                fields=['created'],
            ),


    'a_cs': {'fields': ['a_cs']},



    'a_en': {'fields': ['a_en']},


    }
    """,
    )