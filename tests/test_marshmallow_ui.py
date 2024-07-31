import os
import re

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model

from oarepo_model_builder.fs import InMemoryFileSystem


def test_generated_schema_ui():
    schema = load_model(
        "test.yaml",
        model_content={

            "settings": {
                "i18n-languages": ["cs", "en"],
                "supported-langs": {"cs": {}, "en": {}},
            },
            "record": {
                "module": {"qualified": "test"},
                "properties": {
                    "a": {
                        "type": "multilingual",
                        "ui": {
                            "marshmallow": {
                                "field-class": "test.FieldClassa",
                                "arguments": ["test=cosi"],
                            }
                        },
                    },
                    "b": {
                        "type": "i18nStr",
                        "ui": {
                            "marshmallow": {
                                "arguments": ["test=cosi"],
                            }
                        },
                        "multilingual": {
                            "lang-field": "language",
                            "value-field": "hodnota",
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

    data = builder.filesystem.open(
        os.path.join("test", "services", "records", "ui_schema.py")
    ).read()
    print(data)

    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """

import marshmallow as ma

from oarepo_runtime.services.schema.i18n_ui import I18nStrUIField
from test import FieldClassa

from oarepo_runtime.services.schema.ui import InvenioUISchema



class TestUISchema(InvenioUISchema):
    
     class Meta:
        unknown = ma.RAISE
        
        
    a = FieldClassa(I18nStrUIField(), test=cosi)
    b = I18nStrUIField(test=cosi, lang_field=language, value_field=hodnota)
    """,
    )
