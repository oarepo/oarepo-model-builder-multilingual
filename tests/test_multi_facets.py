import os
import re

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model

from tests.mock_filesystem import MockFilesystem


def test_search_options():
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
        os.path.join("test", "services", "records", "search.py")
    ).read()

    print(data)
    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
from invenio_records_resources.services import SearchOptions as InvenioSearchOptions
from flask_babelex import lazy_gettext as _
from . import facets



class TestSearchOptions(InvenioSearchOptions):
    \"""TestRecord search options.\"""

    facets = {


    '_schema': facets._schema,



    'a_cs': facets.a_cs,



    'a_en': facets.a_en,



    'a_lang': facets.a_lang,



    'a_value': facets.a_value,



    'created': facets.created,



    '_id': facets._id,



    'updated': facets.updated,
    
    **getattr(InvenioSearchOptions, 'facets', {})


    }
    sort_options = {
        
        **InvenioSearchOptions.sort_options,
        

    }
    """,
    )


def test_facets():
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
                "properties": {
                    "d": {
                        "use": "i18n",
                        "properties": {
                            "navic": {
                                "type": "object",
                                "properties": {"kxh": {"type": "keyword"}},
                            }
                        },
                    },
                    "b": "keyword",
                    "c": {
                        "type": "i18nStr",
                        "multilingual": {"lang-field": "language"},
                    },
                    "a": {"type": "multilingual"},
                    "e": {
                        "type": "object",
                        "properties": {"f": "keyword", "g": "i18nStr"},
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
        os.path.join("test", "services", "records", "facets.py")
    ).read()

    print(data)
    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
\"""Facet definitions.\"""

from invenio_search.engine import dsl
from flask_babelex import lazy_gettext as _

from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.facets.date import DateTimeFacet
from oarepo_runtime.facets.nested_facet import NestedLabeledFacet



_schema = TermsFacet(field='$schema', label =_('$schema.label'))

a_cs = TermsFacet(field='a.cs.keyword', label =_('a.label'))

a_en = TermsFacet(field='a.en.keyword', label =_('a.label'))

a_lang = NestedLabeledFacet(path = 'a', nested_facet = TermsFacet(field='a.lang', label =_('a/lang.label')))

a_value = NestedLabeledFacet(path = 'a', nested_facet = TermsFacet(field='a.value.keyword', label =_('a/value.label')))

b = TermsFacet(field='b', label =_('b.label'))

c_cs = TermsFacet(field='c.cs.keyword', label =_('c.label'))

c_en = TermsFacet(field='c.en.keyword', label =_('c.label'))

c_language = NestedLabeledFacet(path = 'c', nested_facet = TermsFacet(field='c.language', label =_('c/language.label')))

c_value = NestedLabeledFacet(path = 'c', nested_facet = TermsFacet(field='c.value.keyword', label =_('c/value.label')))

created = DateTimeFacet(field='created', label =_('created.label'))

d_cs = TermsFacet(field='d.cs.keyword', label =_('d.label'))

d_en = TermsFacet(field='d.en.keyword', label =_('d.label'))

d_lang = NestedLabeledFacet(path = 'd', nested_facet = TermsFacet(field='d.lang', label =_('d/lang.label')))

d_navic_kxh = NestedLabeledFacet(path = 'd', nested_facet = TermsFacet(field='d.navic.kxh', label =_('d/navic/kxh.label')))

d_value = NestedLabeledFacet(path = 'd', nested_facet = TermsFacet(field='d.value.keyword', label =_('d/value.label')))

e_f = TermsFacet(field='e.f', label =_('e/f.label'))

e_g_cs = TermsFacet(field='e.g.cs.keyword', label =_('e/g.label'))

e_g_en = TermsFacet(field='e.g.en.keyword', label =_('e/g.label'))

e_g_lang = NestedLabeledFacet(path = 'e.g', nested_facet = TermsFacet(field='e.g.lang', label =_('e/g/lang.label')))

e_g_value = NestedLabeledFacet(path = 'e.g', nested_facet = TermsFacet(field='e.g.value.keyword', label =_('e/g/value.label')))

_id = TermsFacet(field='id', label =_('id.label'))

updated = DateTimeFacet(field='updated', label =_('updated.label'))




























    """,
    )
