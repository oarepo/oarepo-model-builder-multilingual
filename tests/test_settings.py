import os
import re

from oarepo_model_builder.entrypoints import load_model, create_builder_from_entrypoints
from tests.mock_filesystem import MockFilesystem

def test_pyproject():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={"oarepo:use": "invenio", "settings": {"supported-langs": ["cs"]},
                       "model": {"properties": {"a": {"type": "multilingual"}}}},
        isort=False,
        black=False,
    )

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = builder.filesystem.open(os.path.join( "pyproject.toml")).read()

    assert """[tool.poetry.dependencies.deepmerge]
version = "^1.0.1"
""" in data

    assert """[tool.poetry.dependencies.langcodes]
version = "^3.3.0"
""" in data
