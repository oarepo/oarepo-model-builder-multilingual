import importlib_metadata
from flask_resources import ResponseHandler
from invenio_records_resources.resources import RecordResourceConfig
from model.resources.records.ui import ModelUIJSONSerializer


class ModelResourceConfig(RecordResourceConfig):
    """ModelRecord resource config."""

    blueprint_name = "Model"
    url_prefix = "/model/"

    @property
    def response_handlers(self):
        entrypoint_response_handlers = {}
        for x in importlib_metadata.entry_points(
            group="invenio.model.response_handlers"
        ):
            entrypoint_response_handlers.update(x.load())
        return {
            "application/vnd.inveniordm.v1+json": ResponseHandler(
                ModelUIJSONSerializer()
            ),
            **super().response_handlers,
            **entrypoint_response_handlers,
        }
