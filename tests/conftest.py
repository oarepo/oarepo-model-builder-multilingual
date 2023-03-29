# import os
#
# import pytest
# from invenio_app.factory import create_api
#
#
# @pytest.fixture(scope="module")
# def create_app(instance_path, entry_points):
#     """Application factory fixture."""
#     return create_api
#
#
# @pytest.fixture(scope="module")
# def app_config(app_config):
#     """Mimic an instance's configuration."""
#     # app_config["JSONSCHEMAS_HOST"] = "localhost"
#     app_config[
#         "RECORDS_REFRESOLVER_CLS"
#     ] = "invenio_records.resolver.InvenioRefResolver"
#     app_config[
#         "RECORDS_REFRESOLVER_STORE"
#     ] = "invenio_jsonschemas.proxies.current_refresolver_store"
#     app_config["RATELIMIT_AUTHENTICATED_USER"] = "200 per second"
#     app_config["SEARCH_HOSTS"] = [
#         {
#             "host": os.environ.get("OPENSEARCH_HOST", "localhost"),
#             "port": os.environ.get("OPENSEARCH_PORT", "9200"),
#         }
#     ]
#
#
#
#     return app_config