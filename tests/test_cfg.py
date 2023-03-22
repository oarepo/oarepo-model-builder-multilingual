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


    assert "deepmerge>=1.1.0" in data
