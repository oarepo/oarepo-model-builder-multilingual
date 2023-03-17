import os
import re

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model

from tests.mock_filesystem import MockFilesystem


def test_search_options():
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
                "properties": {"a": {"type": "multilingual", "sortable": {}}},
            },
        },
        isort=False,
        black=False,
    )

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = builder.filesystem.open(
        os.path.join("test", "services", "records", "search.py")
    ).read()

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


    'a_lang': facets.a_lang,



    'a_cs': facets.a_cs,



    'a_en': facets.a_en,



    'a_value_keyword': facets.a_value_keyword,



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


    }
    """,
    )


def test_facets():
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
                    "a": {"type": "multilingual", "sortable": {}},
                    "e": {
                        "type": "object",
                        "properties": {"f": "keyword", "g": "i18nStr"},
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
        os.path.join("test", "services", "records", "facets.py")
    ).read()

    print(data)
    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
\"""Facet definitions.\"""

from invenio_records_resources.services.records.facets import TermsFacet
from invenio_search.engine import dsl
from oarepo_runtime.facets.nested_facet import NestedLabeledFacet




d_navic_kxh = NestedLabeledFacet(path ="d", nested_facet = TermsFacet(field="d.navic.kxh"))



d_lang = NestedLabeledFacet(path ="d", nested_facet = TermsFacet(field="d.lang"))



d_cs = TermsFacet(field="d_cs")



d_en = TermsFacet(field="d_en")



d_value_keyword = NestedLabeledFacet(path ="d", nested_facet = TermsFacet(field="d.value.keyword"))



b = TermsFacet(field="b")



c_language = NestedLabeledFacet(path ="c", nested_facet = TermsFacet(field="c.language"))



c_cs = TermsFacet(field="c_cs")



c_en = TermsFacet(field="c_en")



c_value_keyword = NestedLabeledFacet(path ="c", nested_facet = TermsFacet(field="c.value.keyword"))



a_lang = NestedLabeledFacet(path ="a", nested_facet = TermsFacet(field="a.lang"))



a_cs = TermsFacet(field="a_cs")



a_en = TermsFacet(field="a_en")



a_value_keyword = NestedLabeledFacet(path ="a", nested_facet = TermsFacet(field="a.value.keyword"))



e_f = TermsFacet(field="e.f")



e_g_lang = NestedLabeledFacet(path ="e.g", nested_facet = TermsFacet(field="e.g.lang"))



e_g_cs = TermsFacet(field="e.g_cs")



e_g_en = TermsFacet(field="e.g_en")



e_g_value_keyword = NestedLabeledFacet(path ="e.g", nested_facet = TermsFacet(field="e.g.value.keyword"))



_id = TermsFacet(field="id")



created = TermsFacet(field="created")



updated = TermsFacet(field="updated")



_schema = TermsFacet(field="$schema")

    """,
    )
