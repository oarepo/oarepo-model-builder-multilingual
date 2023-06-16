from oarepo_model_builder.entrypoints import load_model

DUMMY_YAML = "test.yaml"


def basic_schema():
    return load_model(
        DUMMY_YAML,
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
            "record": {
                "use": "invenio",
                "module": {"qualified": "test"},
                "properties": {"a": {"type": "multilingual"}},
            },
        },
        isort=False,
        black=False,
        autoflake=False,
    )
