from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model

from tests.mock_filesystem import MockFilesystem


def test_validity():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={
            "settings": {
                "supported-langs": {
                    "en": {
                        "text": {"analyzer": "czech"},
                        "sort": {"type": "icu_collation_keyword"},
                    }
                }
            },
            "model": {
                "use": "invenio",
                "properties": {"a": {"type": "multilingual", "ui": {}}},
            },
        },
        isort=False,
        black=False,
    )

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")
