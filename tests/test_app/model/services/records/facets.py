"""Facet definitions."""

from invenio_records_resources.services.records.facets import TermsFacet
from invenio_search.engine import dsl
from oarepo_runtime.facets.nested_facet import NestedLabeledFacet

metadata_a_lang = NestedLabeledFacet(
    path="metadata.a", nested_facet=TermsFacet(field="metadata.a.lang")
)


metadata_a_cs_keyword = TermsFacet(field="metadata.a_cs.keyword")


metadata_a_en_keyword = TermsFacet(field="metadata.a_en.keyword")


metadata_a_value_keyword = NestedLabeledFacet(
    path="metadata.a", nested_facet=TermsFacet(field="metadata.a.value.keyword")
)


_id = TermsFacet(field="id")


created = TermsFacet(field="created")


updated = TermsFacet(field="updated")


_schema = TermsFacet(field="$schema")
