"""Facet definitions."""

from flask_babelex import lazy_gettext as _
from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.facets.date import DateTimeFacet
from oarepo_runtime.facets.nested_facet import NestedLabeledFacet

metadata_a_lang = NestedLabeledFacet(
    path="metadata.a",
    nested_facet=TermsFacet(field="metadata.a.lang", label=_("metadata/a/lang.label")),
)


metadata_a_cs_keyword = TermsFacet(field="metadata.a_cs.keyword")


metadata_a_en_keyword = TermsFacet(field="metadata.a_en.keyword")


metadata_a_value_keyword = NestedLabeledFacet(
    path="metadata.a",
    nested_facet=TermsFacet(
        field="metadata.a.value.keyword", label=_("metadata/a/value/keyword.label")
    ),
)


_id = TermsFacet(field="id", label=_("id.label"))


created = DateTimeFacet(field="created", label=_("created.label"))


updated = DateTimeFacet(field="updated", label=_("updated.label"))


_schema = TermsFacet(field="$schema", label=_("$schema.label"))
