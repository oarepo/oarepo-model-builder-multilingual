"""Facet definitions."""

from flask_babelex import lazy_gettext as _
from invenio_records_resources.services.records.facets import TermsFacet
from oarepo_runtime.facets.date import DateTimeFacet
from oarepo_runtime.facets.nested_facet import NestedLabeledFacet

_schema = TermsFacet(field="$schema", label=_("$schema.label"))

created = DateTimeFacet(field="created", label=_("created.label"))

_id = TermsFacet(field="id", label=_("id.label"))

metadata_a_cs = TermsFacet(field="metadata.a.cs.keyword", label=_("metadata/a.label"))

metadata_a_en = TermsFacet(field="metadata.a.en.keyword", label=_("metadata/a.label"))

metadata_a_lang = NestedLabeledFacet(
    path="metadata.a",
    nested_facet=TermsFacet(field="metadata.a.lang", label=_("metadata/a/lang.label")),
)

metadata_a_value = NestedLabeledFacet(
    path="metadata.a",
    nested_facet=TermsFacet(
        field="metadata.a.value.keyword", label=_("metadata/a/value.label")
    ),
)

updated = DateTimeFacet(field="updated", label=_("updated.label"))
