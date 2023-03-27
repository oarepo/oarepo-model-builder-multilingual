from invenio_records_resources.services import SearchOptions as InvenioSearchOptions

from . import facets


def _(x):
    """Identity function for string extraction."""
    return x


class ModelSearchOptions(InvenioSearchOptions):
    """ModelRecord search options."""

    facets = {
        "metadata_a_lang": facets.metadata_a_lang,
        "metadata_a_cs_keyword": facets.metadata_a_cs_keyword,
        "metadata_a_en_keyword": facets.metadata_a_en_keyword,
        "metadata_a_value_keyword": facets.metadata_a_value_keyword,
        "_id": facets._id,
        "created": facets.created,
        "updated": facets.updated,
        "_schema": facets._schema,
    }
    sort_options = {
        **InvenioSearchOptions.sort_options,
        "bestmatch": dict(
            title=_("Best match"),
            fields=["_score"],  # ES defaults to desc on `_score` field
        ),
        "newest": dict(
            title=_("Newest"),
            fields=["-created"],
        ),
        "oldest": dict(
            title=_("Oldest"),
            fields=["created"],
        ),
    }
