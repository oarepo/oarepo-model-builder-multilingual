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
from flask_babelex import lazy_gettext as _
from . import facets



class TestSearchOptions(InvenioSearchOptions):
    \"""TestRecord search options.\"""

    facets = {


    'a_lang': facets.a_lang,



    'a_cs_keyword': facets.a_cs_keyword,



    'a_en_keyword': facets.a_en_keyword,



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

from invenio_search.engine import dsl
from flask_babelex import lazy_gettext as _



from invenio_records_resources.services.records.facets import TermsFacet



from oarepo_runtime.facets.date import DateTimeFacet



from oarepo_runtime.facets.nested_facet import NestedLabeledFacet






d_navic_kxh = NestedLabeledFacet(path ="d", nested_facet = TermsFacet(field="d.navic.kxh", label=_("d/navic/kxh.label")))



d_lang = NestedLabeledFacet(path ="d", nested_facet = TermsFacet(field="d.lang", label=_("d/lang.label")))



d_cs_keyword = TermsFacet(field="d_cs.keyword")



d_en_keyword = TermsFacet(field="d_en.keyword")



d_value_keyword = NestedLabeledFacet(path ="d", nested_facet = TermsFacet(field="d.value.keyword", label=_("d/value/keyword.label")))



b = TermsFacet(field="b", label=_("b.label"))



c_language = NestedLabeledFacet(path ="c", nested_facet = TermsFacet(field="c.language", label=_("c/language.label")))



c_cs_keyword = TermsFacet(field="c_cs.keyword")



c_en_keyword = TermsFacet(field="c_en.keyword")



c_value_keyword = NestedLabeledFacet(path ="c", nested_facet = TermsFacet(field="c.value.keyword", label=_("c/value/keyword.label")))



a_lang = NestedLabeledFacet(path ="a", nested_facet = TermsFacet(field="a.lang", label=_("a/lang.label")))



a_cs_keyword = TermsFacet(field="a_cs.keyword")



a_en_keyword = TermsFacet(field="a_en.keyword")



a_value_keyword = NestedLabeledFacet(path ="a", nested_facet = TermsFacet(field="a.value.keyword", label=_("a/value/keyword.label")))



e_f = TermsFacet(field="e.f", label=_("e/f.label"))



e_g_lang = NestedLabeledFacet(path ="e.g", nested_facet = TermsFacet(field="e.g.lang", label=_("e/g/lang.label")))



e_g_cs_keyword = TermsFacet(field="e.g_cs.keyword")



e_g_en_keyword = TermsFacet(field="e.g_en.keyword")



e_g_value_keyword = NestedLabeledFacet(path ="e.g", nested_facet = TermsFacet(field="e.g.value.keyword", label=_("e/g/value/keyword.label")))



_id = TermsFacet(field="id", label=_("id.label"))



created = DateTimeFacet(field="created", label=_("created.label"))



updated = DateTimeFacet(field="updated", label=_("updated.label"))



_schema = TermsFacet(field="$schema", label=_("$schema.label"))

    """,
    )
