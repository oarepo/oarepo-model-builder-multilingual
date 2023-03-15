from oarepo_model_builder.entrypoints import load_model

DUMMY_YAML = "test.yaml"


def basic_schema():
    return load_model(
        DUMMY_YAML,
        "test",
        model_content={
            "settings": {
                "supported-langs": {
                    "cs": {
                        "text": {
                            "analyzer": "czech",
                        },
                        "sort": {"type": "icu_collation_keyword"},
                    },
                    "en": {
                        "text": {"analyzer": "en"},
                        "sort": {"type": "icu_collation_keyword"},
                    },
                }
            },
            "model": {"use": "invenio", "properties": {"a": {"type": "multilingual"}}},
        },
        isort=False,
        black=False,
    )
