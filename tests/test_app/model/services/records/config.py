from invenio_records_resources.services import RecordLink
from invenio_records_resources.services import RecordServiceConfig
from invenio_records_resources.services import pagination_links
from model.records.api import ModelRecord
from model.services.records.permissions import ModelPermissionPolicy
from model.services.records.schema import ModelSchema
from model.services.records.search import ModelSearchOptions
from oarepo_runtime.relations.components import CachingRelationsComponent


class ModelServiceConfig(RecordServiceConfig):
    """ModelRecord service config."""

    url_prefix = "/model/"

    permission_policy_cls = ModelPermissionPolicy

    schema = ModelSchema

    search = ModelSearchOptions

    record_cls = ModelRecord
    service_id = "model"

    components = [*RecordServiceConfig.components, CachingRelationsComponent]

    model = "model"

    @property
    def links_item(self):
        return {
            "self": RecordLink("{self.url_prefix}{id}"),
        }

    @property
    def links_search(self):
        return pagination_links("{self.url_prefix}{?args*}")
