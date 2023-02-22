from oarepo_model_builder.entrypoints import load_model


def basic_schema():
    return load_model(
        "test.yaml",
        "test",
        model_content={
            "use": "invenio",
            "supported-langs": {
                "cs": {
                    "text": {
                        "analyzer": "czech",
                    },
                    "sort": {"type": "icu_collation_keyword"},
                    "keyword": {"test": "test"},
                },
                "en": {
                    "text": {"analyzer": "en"},
                    "sort": {"type": "icu_collation_keyword"},
                },
            },
            "model": {"properties": {"a": {"type": "multilingual"}}},
        },
        isort=False,
        black=False,
    )
