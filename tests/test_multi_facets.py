import os
import re

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model

from oarepo_model_builder.fs import InMemoryFileSystem


def test_search_options():
    schema = load_model(
        "test.yaml",
        model_content={
            "settings": {
                "i18n-languages": ["cs", "en"],
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

    filesystem = InMemoryFileSystem()
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
from oarepo_runtime.i18n import lazy_gettext as _
from . import facets

class TestSearchOptions(InvenioSearchOptions):
    \"""TestRecord search options.\"""

    facet_groups={}

    facets = {


    **getattr(InvenioSearchOptions, 'facets', {}), 'a_cs': facets.a_cs,



    'a_en': facets.a_en,



    'a': facets.a,



    'a_lang': facets.a_lang,



    

    }
    """,
    )


def test_facets():
    schema = load_model(
        "test.yaml",
        model_content={
            "settings": {
                "i18n-languages": ["cs", "en"],
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

    filesystem = InMemoryFileSystem()
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
from oarepo_runtime.i18n import lazy_gettext as _

from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.services.facets import MultilingualFacet
from oarepo_runtime.services.facets.nested_facet import NestedLabeledFacet



a_cs = TermsFacet(field='a_cs.keyword', label =_('a.label'))

a_en = TermsFacet(field='a_en.keyword', label =_('a.label'))

a = MultilingualFacet(lang_facets={ 'cs': a_cs, 'en': a_en }, label=_('a.label'))

a_lang = NestedLabeledFacet(path = 'a', nested_facet = TermsFacet(field='a.lang', label =_('a/lang.label')))

b = TermsFacet(field='b', label =_('b.label'))

c_cs = TermsFacet(field='c_cs.keyword', label =_('c.label'))

c_en = TermsFacet(field='c_en.keyword', label =_('c.label'))

c = MultilingualFacet(lang_facets={ 'cs': c_cs, 'en': c_en }, label=_('c.label'))

c_language = NestedLabeledFacet(path = 'c', nested_facet = TermsFacet(field='c.language', label =_('c/language.label')))

d_cs = TermsFacet(field='d_cs.keyword', label =_('d.label'))

d_en = TermsFacet(field='d_en.keyword', label =_('d.label'))

d = MultilingualFacet(lang_facets={ 'cs': d_cs, 'en': d_en }, label=_('d.label'))

d_lang = NestedLabeledFacet(path = 'd', nested_facet = TermsFacet(field='d.lang', label =_('d/lang.label')))

d_navic_kxh = NestedLabeledFacet(path = 'd', nested_facet = TermsFacet(field='d.navic.kxh', label =_('d/navic/kxh.label')))

e_f = TermsFacet(field='e.f', label =_('e/f.label'))

e_g_cs = TermsFacet(field='e.g_cs.keyword', label =_('e/g.label'))

e_g_en = TermsFacet(field='e.g_en.keyword', label =_('e/g.label'))

e_g = MultilingualFacet(lang_facets={ 'cs': e_g_cs, 'en': e_g_en }, label=_('e/g.label'))

e_g_lang = NestedLabeledFacet(path = 'e.g', nested_facet = TermsFacet(field='e.g.lang', label =_('e/g/lang.label')))




























    """,
    )
