from invenio_records_resources.services import RecordLink
from invenio_records_resources.services import (
    RecordServiceConfig as InvenioRecordServiceConfig,
)
from invenio_records_resources.services import pagination_links
from oarepo_runtime.config.service import PermissionsPresetsConfigMixin

from oarepo_model_builder_multilingual.records.api import (
    OarepoModelBuilderMultilingualRecord,
)
from oarepo_model_builder_multilingual.services.records.permissions import (
    OarepoModelBuilderMultilingualPermissionPolicy,
)
from oarepo_model_builder_multilingual.services.records.schema import (
    OarepoModelBuilderMultilingualSchema,
)
from oarepo_model_builder_multilingual.services.records.search import (
    OarepoModelBuilderMultilingualSearchOptions,
)


class OarepoModelBuilderMultilingualServiceConfig(
    PermissionsPresetsConfigMixin, InvenioRecordServiceConfig
):
    """OarepoModelBuilderMultilingualRecord service config."""

    PERMISSIONS_PRESETS = ["everyone"]

    url_prefix = "/oarepo-model-builder-multilingual/"

    base_permission_policy_cls = OarepoModelBuilderMultilingualPermissionPolicy

    schema = OarepoModelBuilderMultilingualSchema

    search = OarepoModelBuilderMultilingualSearchOptions

    record_cls = OarepoModelBuilderMultilingualRecord

    service_id = "oarepo_model_builder_multilingual"

    components = [
        *PermissionsPresetsConfigMixin.components,
        *InvenioRecordServiceConfig.components,
    ]

    model = "oarepo_model_builder_multilingual"

    @property
    def links_item(self):
        return {
            "self": RecordLink("{+api}/oarepo-model-builder-multilingual/{id}"),
        }

    @property
    def links_search(self):
        return {
            **pagination_links("{+api}/oarepo-model-builder-multilingual/{?args*}"),
        }
