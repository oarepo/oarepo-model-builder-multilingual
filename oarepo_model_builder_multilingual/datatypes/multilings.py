from oarepo_model_builder.datatypes import DataType
from oarepo_model_builder.datatypes.containers import ArrayDataType, NestedDataType
from oarepo_model_builder.utils.deepmerge import deepmerge


class MultilingualDataType(ArrayDataType):
    schema_type = "array"
    mapping_type = "multilingual"
    marshmallow_field = "ma_fields.List"
    model_type = "multilingual"

    class ModelSchema(DataType.ModelSchema):
        pass

    def prepare(self, context):
        definition = self.definition

        definition["type"] = "array"
        definition["items"] = {"type": "i18nStr", "multilingual": definition.get("multilingual", {})}
        definition_marsh = definition.get("marshmallow", {})
        if "field-class" not in definition_marsh:
            definition_marsh["field-class"] = (
                "oarepo_runtime.services.schema.i18n.MultilingualField"
            )
        deepmerge(definition, {"marshmallow": definition_marsh})

        definition_ui = definition.get("ui", {})
        definition_ui_marsh = definition_ui.get("marshmallow", {})
        if "detail" not in definition_ui:
            definition_ui["detail"] = "multilingual"

        if "field-class" not in definition_ui_marsh:
            definition_ui_marsh["field-class"] = (
                "oarepo_runtime.services.schema.i18n_ui.MultilingualUIField"
            )
        deepmerge(definition_ui, {"marshmallow": definition_ui_marsh})
        deepmerge(definition, {"ui": definition_ui})
        super().prepare(context)


class I18nDataType(NestedDataType):
    schema_type = "object"
    mapping_type = "i18nStr"
    marshmallow_field = "ma_fields.Nested"
    model_type = "i18nStr"
    json_schema_type = "nested"

    class ModelSchema(
        NestedDataType.ModelSchema,
    ):
        pass

    def prepare(self, context):
        definition = self.definition
        mult_definition = definition.get("multilingual", {})
        lang = mult_definition.get("lang_field", "lang")
        value = mult_definition.get("value_field", "value")
        definition["type"] = "i18nStr"

        """marshmallow"""

        definition_marsh = definition.get("marshmallow", {})
        if "schema-class" not in definition_marsh:
            definition_marsh["class"] = None
        if "field-class" not in definition_marsh:
            definition_marsh["field-class"] = (
                "oarepo_runtime.services.schema.i18n.I18nStrField"
            )

        if "generate" not in definition_marsh:
            definition_marsh["generate"] = False

        if "lang_field" in mult_definition:
            if "arguments" not in definition_marsh:
                definition_marsh["arguments"] = [
                    f'lang_field={mult_definition["lang_field"]}'
                ]
            else:
                definition_marsh["arguments"].append(
                    f'lang_field={mult_definition["lang_field"]}'
                )
        if "value_field" in mult_definition:
            if "arguments" not in definition_marsh:
                definition_marsh["arguments"] = [
                    f'value_field={mult_definition["value_field"]}'
                ]
            else:
                definition_marsh["arguments"].append(
                    f'value_field={mult_definition["value_field"]}'
                )
        deepmerge(definition, {"marshmallow": definition_marsh})

        """marshmallow ui"""

        definition_ui = definition.get("ui", {})
        definition_ui_marsh = definition_ui.get("marshmallow", {})
        if "detail" not in definition_ui:
            definition_ui["detail"] = "multilingual"
        if "schema-class" not in definition_ui_marsh:
            definition_ui_marsh["class"] = None
        if "field-class" not in definition_ui_marsh:
            definition_ui_marsh["field-class"] = (
                "oarepo_runtime.services.schema.i18n_ui.I18nStrUIField"
            )

        if "lang_field" in mult_definition:
            if "arguments" not in definition_ui_marsh:
                definition_ui_marsh["arguments"] = [
                    f'lang_field={mult_definition["lang_field"]}'
                ]
            else:
                definition_ui_marsh["arguments"].append(
                    f'lang_field={mult_definition["lang_field"]}'
                )
        if "value_field" in mult_definition:
            if "arguments" not in definition_ui_marsh:
                definition_ui_marsh["arguments"] = [
                    f'value_field={mult_definition["value_field"]}'
                ]
            else:
                definition_ui_marsh["arguments"].append(
                    f'value_field={mult_definition["value_field"]}'
                )

        deepmerge(definition_ui, {"marshmallow": definition_ui_marsh})
        deepmerge(definition, {"ui": definition_ui})

        def_properties = definition.get("properties", {})
        definition["sample"] = {"skip": False}

        lang_definition, value_definition = labels(mult_definition)

        def_properties[lang] = {
            "type": "keyword",
            "mapping": {"ignore_above": 256},
            "required": True,
        }
        deepmerge(def_properties[lang], lang_definition)

        def_properties[value] = {"type": "fulltext+keyword", "required": True}
        deepmerge(def_properties[value], value_definition)

        definition["properties"] = def_properties

        super().prepare(context)


def labels(mult_definition):
    definition = {
        "lang_def": {
            "label.cs": mult_definition.get("lang_def", {}).get("label.cs", "Jazyk"),
            "label.en": mult_definition.get("lang_def", {}).get("label.en", "Language"),
        },
        "value_def": {
            "label.cs": mult_definition.get("value_def", {}).get("label.cs", "Text"),
            "label.en": mult_definition.get("value_def", {}).get("label.en", "Text"),
        },
    }
    deepmerge(mult_definition, definition)

    lang_definition = {}
    value_definition = {}

    langs = mult_definition.get("lang_def", {})
    for key, value in langs.items():
        lang_definition[key] = value

    values = mult_definition.get("value_def", {})
    for key, value in values.items():
        value_definition[key] = value

    return lang_definition, value_definition
