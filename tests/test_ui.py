import os

import json5
from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model

from oarepo_model_builder.fs import InMemoryFileSystem

def test_model():
    schema = load_model(
        "test.yaml",
        model_content={
            "settings": {
                "supported-langs": {
                    "en": {
                        "text": {"analyzer": "czech"},
                        "sort": {"type": "icu_collation_keyword"},
                    }
                },
                "i18n-languages": ["cs", "en"],
            },
            "record": {
                "use": "invenio",
                "module": {"qualified": "test"},
                "properties": {
                    "b": {"type": "keyword", "label.en": "kchhh", "label.cs": "jej"},
                    "a": {
                        "type": "multilingual",
                        "ui": {},
                        "label.en": "multilabel.en",
                        "label.cs": "multilabel.cs",
                        "multilingual": {
                            "labels": {"lang_cs": "vlastni Jazyk2", "lang_en": "vlastni Language2"},
                            "helps": {"value_cs": "vlastni Napoveda value", "lang_en": "vlastni Help language"},
                        },
                    },
                    "c": {
                        "type": "i18nStr",
                        "ui": {},
                        "label.en": "multilabel.en",
                        "label.cs": "multilabel.cs",
                        "multilingual": {
                            "labels": {"lang_cs": "Jazyk2", "lang_en": "Language2"},
                            "helps": {"lang_cs": "Napoveda", "lang_en": "Help"},
                        },
                    },
                },
            },
        },
        isort=False,
        black=False,
        autoflake=False,
    )

    filesystem = InMemoryFileSystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "record", ["record"], "")
    data = json5.load(
        builder.filesystem.open(os.path.join("test", "models", "records.json"))
    )
    print(data["model"]["properties"]["a"])
    assert data["model"]["properties"]["a"] == {
        'type': 'array', 'ui': {'detail': 'multilingual', 'marshmallow': {
            'field-class': 'oarepo_runtime.services.schema.i18n_ui.MultilingualUIField'}}, 'multilingual': {
            'labels': {'lang_cs': 'vlastni Jazyk2', 'lang_en': 'vlastni Language2', 'value_cs': 'Text',
                       'value_en': 'Text'},
            'helps': {'value_cs': 'vlastni Napoveda value', 'lang_en': 'vlastni Help language'}},
        'label.en': 'multilabel.en', 'label.cs': 'multilabel.cs',
        'marshmallow': {'field-class': 'oarepo_runtime.services.schema.i18n.MultilingualField'},
        'items': {'type': 'i18nStr', 'multilingual': {
            'labels': {'lang_cs': 'vlastni Jazyk2', 'lang_en': 'vlastni Language2', 'value_cs': 'Text',
                       'value_en': 'Text'},
            'helps': {'value_cs': 'vlastni Napoveda value', 'lang_en': 'vlastni Help language'}},
                  'marshmallow': {'class': None, 'field-class': 'oarepo_runtime.services.schema.i18n.I18nStrField',
                                  'generate': False}, 'ui': {'detail': 'multilingual', 'marshmallow': {'class': None,
                                                                                                       'field-class': 'oarepo_runtime.services.schema.i18n_ui.I18nStrUIField'}},
                  'sample': {'skip': False}, 'properties': {
                'lang': {'type': 'keyword', 'mapping': {'ignore_above': 256}, 'required': True,
                         'label.cs': 'vlastni Jazyk2', 'label.en': 'vlastni Language2',
                         'help.en': 'vlastni Help language'},
                'value': {'type': 'fulltext+keyword', 'required': True, 'label.cs': 'Text', 'label.en': 'Text',
                          'help.cs': 'vlastni Napoveda value'}}}}

    assert data["model"]["properties"]["b"] == {
        "type": "keyword",
        "label.en": "kchhh",
        "label.cs": "jej",
    }

    assert data["model"]["properties"]["c"] == {
        "type": "i18nStr",
        "ui": {
            "detail": "multilingual",
            "marshmallow": {
                "class": None,
                "field-class": "oarepo_runtime.services.schema.i18n_ui.I18nStrUIField",
            },
        },
        "multilingual": {
            "labels": {
                "lang_cs": "Jazyk2",
                "lang_en": "Language2",
                "value_cs": "Text",
                "value_en": "Text",
            },
            "helps": {"lang_cs": "Napoveda", "lang_en": "Help"},
        },
        "label.en": "multilabel.en",
        "label.cs": "multilabel.cs",
        "marshmallow": {
            "class": None,
            "field-class": "oarepo_runtime.services.schema.i18n.I18nStrField",
            "generate": False,
        },
        "sample": {"skip": False},
        "properties": {
            "lang": {
                "type": "keyword",
                "mapping": {"ignore_above": 256},
                "required": True,
                "label.cs": "Jazyk2",
                "label.en": "Language2",
                "help.cs": "Napoveda",
                "help.en": "Help",
            },
            "value": {'label.cs': 'Text',
                          'label.en': 'Text',
                          'required': True,
                          'type': 'fulltext+keyword'},
        },
    }
