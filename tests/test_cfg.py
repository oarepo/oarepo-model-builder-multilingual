import json
import os
import re

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints
from oarepo_model_builder.fs import InMemoryFileSystem

from tests.test_helper import basic_schema


def test_json():
    schema = basic_schema()

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = builder.filesystem.open(
        os.path.join( "setup.cfg")
    ).read()
    print(data)

    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """
        [metadata]
name = test
version = 1.0.0
description = A sample application for test
authors = 


[options]
python = >=3.9
install_requires =
    invenio_access>=1.4.4
    invenio_app>=1.3.4
    invenio_db>=1.0.14
    invenio_pidstore>=1.2.3
    invenio_records>=2.0.0
    invenio-records-rest>=2.1.0
    invenio_records_permissions>=0.13.0
    invenio_records_resources>=0.21.4
    invenio-search>=2.1.0
    tqdm>=4.64.1
    oarepo-runtime>=1.0.0
    deepmerge>=1.1.0
packages = find:


[options.package_data]
* = *.json, *.rst, *.md, *.json5, *.jinja2


[options.entry_points]
invenio_base.api_apps = test = test.ext:TestExt
invenio_base.apps = test = test.ext:TestExt
invenio_db.alembic = test = test:alembic
invenio_db.models = test = test.records.models
invenio_base.api_blueprints = test = test.views:create_blueprint_from_app_test
invenio_base.blueprints = test = test.views:create_blueprint_from_app_testExt
invenio_search.mappings = test = test.records.mappings
invenio_jsonschemas.schemas = test = test.records.jsonschemas
oarepo.models = test = test.models:model.json
flask.commands = test = test.cli:group


[options.extras_require]
tests =
    invenio-app>=1.3.3
    invenio-db[postgresql,mysql,versioning]>=1.0.14,<2.0.0
    pytest-invenio>=1.4.11
    invenio_search[opensearch2]>=2.0.0
    Werkzeug<2.2.0
    Flask-Login>=0.6.1
    pyyaml>=6.0
    requests>=2.28.1
        """)