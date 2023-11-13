from invenio_records_resources.services import SearchOptions as InvenioSearchOptions

from . import facets


class OarepoModelBuilderMultilingualSearchOptions(InvenioSearchOptions):
    """OarepoModelBuilderMultilingualRecord search options."""

    facet_groups = {}

    facets = {
        "_schema": facets._schema,
        "created": facets.created,
        "_id": facets._id,
        "metadata_a_cs": facets.metadata_a_cs,
        "metadata_a_en": facets.metadata_a_en,
        "metadata_a_lang": facets.metadata_a_lang,
        "metadata_a_value": facets.metadata_a_value,
        "updated": facets.updated,
        **getattr(InvenioSearchOptions, "facets", {}),
    }
