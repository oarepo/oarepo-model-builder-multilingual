import os
import re

from oarepo_model_builder.entrypoints import create_builder_from_entrypoints, load_model

from tests.mock_filesystem import MockFilesystem


def test_generated_schema_ui():
    schema = load_model(
        "test.yaml",
        "test",
        model_content={
            "settings": {
                "supported-langs": {"cs": {}, "en": {}},
            },
            "model": {
                "properties": {
                    "a": {"type": "multilingual", "ui": {
                        "marshmallow": {"imports": [{"import": "test"}], "field-class": "FieldClassa",
                                        "arguments": ["test=cosi"]}}},
                    "b": {"type": "i18nStr", "ui": {
                        "marshmallow": {"imports": [{"import": "test"}],
                                        "arguments": ["test=cosi"]}},
                          "multilingual": {"lang-field": "language", "value-field": "hodnota"}},

                },
            },
        },
        isort=False,
        black=False,
    )

    filesystem = MockFilesystem()
    builder = create_builder_from_entrypoints(filesystem=filesystem)

    builder.build(schema, "")

    data = builder.filesystem.open(
        os.path.join("test", "services", "records", "ui_schema.py")
    ).read()
    print(data)

    assert re.sub(r"\s", "", data) == re.sub(
        r"\s",
        "",
        """

from invenio_records_resources.services.records.schema import BaseRecordSchema as InvenioBaseRecordSchema
from marshmallow import ValidationError
from marshmallow import validate as ma_validate
import marshmallow as ma
from marshmallow import fields as ma_fields
from marshmallow_utils import fields as mu_fields
from marshmallow_utils import schemas as mu_schemas



from oarepo_runtime.i18n.ui_schema import I18nStrUIField



from oarepo_runtime.i18n.ui_schema import MultilingualUIField



from test import test





class TestUISchema(ma.Schema):
    \"""TestUISchema schema.\"""
    a = FieldClassa(I18nStrUIField())
    b = I18nStrUIField(test=cosi, lang_field=language, value_field=hodnota)
    """,
    )
