import importlib_metadata
from flask_resources import ResponseHandler
from invenio_records_resources.resources import RecordResourceConfig

from oarepo_model_builder_multilingual.resources.records.ui import (
    OarepoModelBuilderMultilingualUIJSONSerializer,
)


class OarepoModelBuilderMultilingualResourceConfig(RecordResourceConfig):
    """OarepoModelBuilderMultilingualRecord resource config."""

    blueprint_name = "oarepo_model_builder_multilingual"
    url_prefix = "/oarepo-model-builder-multilingual/"

    @property
    def response_handlers(self):
        entrypoint_response_handlers = {}
        for x in importlib_metadata.entry_points(
            group="invenio.oarepo_model_builder_multilingual.response_handlers"
        ):
            entrypoint_response_handlers.update(x.load())
        return {
            "application/vnd.inveniordm.v1+json": ResponseHandler(
                OarepoModelBuilderMultilingualUIJSONSerializer()
            ),
            **super().response_handlers,
            **entrypoint_response_handlers,
        }
