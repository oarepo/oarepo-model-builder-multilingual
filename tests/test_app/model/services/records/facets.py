"""Facet definitions."""

from invenio_records_resources.services.records.facets import TermsFacet
from invenio_search.engine import dsl
from oarepo_runtime.facets.nested_facet import NestedLabeledFacet

a_lang = NestedLabeledFacet(path="a", nested_facet=TermsFacet(field="a.lang"))


a_cs = TermsFacet(field="a_cs")


a_en = TermsFacet(field="a_en")


a_value_keyword = NestedLabeledFacet(
    path="a", nested_facet=TermsFacet(field="a.value.keyword")
)


_id = TermsFacet(field="id")


created = TermsFacet(field="created")


updated = TermsFacet(field="updated")


_schema = TermsFacet(field="$schema")
