from oarepo_model_builder.datatypes import DataType
from oarepo_model_builder.datatypes.containers import ArrayDataType, NestedDataType
from oarepo_model_builder.utils.deepmerge import deepmerge


def multilingual_definition_update(definition_marsh, mult_definition):
    if "lang-name" in mult_definition:
        if "arguments" not in definition_marsh:
            definition_marsh["arguments"] = [
                f'lang_name={mult_definition["lang-name"]}'
            ]
        else:
            definition_marsh["arguments"].append(
                f'lang_name={mult_definition["lang-name"]}'
            )

    if "value-field" in mult_definition:
        if "arguments" not in definition_marsh:
            definition_marsh["arguments"] = [
                f'value_field={mult_definition["value-field"]}'
            ]
        else:
            definition_marsh["arguments"].append(
                f'value_field={mult_definition["value-field"]}'
            )
    if "value-name" in mult_definition:
        if "arguments" not in definition_marsh:
            definition_marsh["arguments"] = [
                f'value_name={mult_definition["value-name"]}'
            ]
        else:
            definition_marsh["arguments"].append(
                f'value_name={mult_definition["value-name"]}'
            )

    return definition_marsh

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
        definition["items"] = {"type": "i18nStr"}
        definition_marsh = definition.get("marshmallow", {})
        if "field-class" not in definition_marsh:
            definition_marsh[
                "field-class"
            ] = "oarepo_runtime.services.schema.i18n.MultilingualField"
        deepmerge(definition, {"marshmallow": definition_marsh})

        definition_ui = definition.get("ui", {})
        definition_ui_marsh = definition_ui.get("marshmallow", {})
        if "detail" not in definition_ui:
            definition_ui["detail"] = "multilingual"

        if "field-class" not in definition_ui_marsh:
            definition_ui_marsh[
                "field-class"
            ] = "oarepo_runtime.services.schema.i18n_ui.MultilingualUIField"
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

        lang = mult_definition.get("lang-name", "lang")
        value = mult_definition.get("value-name", "value")
        value_type = mult_definition.get("value-type", "html")

        definition["type"] = "i18nStr"

        """marshmallow"""

        definition_marsh = definition.get("marshmallow", {})

        if "schema-class" not in definition_marsh:
            definition_marsh["class"] = None

        if "field-class" not in definition_marsh:
            definition_marsh[
                "field-class"
            ] = "oarepo_runtime.services.schema.i18n.I18nStrField"

        if "generate" not in definition_marsh:
            definition_marsh["generate"] = False

        definition_marsh = multilingual_definition_update(definition_marsh, mult_definition)
        deepmerge(definition, {"marshmallow": definition_marsh})

        """marshmallow ui"""

        definition_ui = definition.get("ui", {})
        definition_ui_marsh = definition_ui.get("marshmallow", {})
        if "detail" not in definition_ui:
            definition_ui["detail"] = "multilingual"
        if "schema-class" not in definition_ui_marsh:
            definition_ui_marsh["class"] = None
        if "field-class" not in definition_ui_marsh:
            definition_ui_marsh[
                "field-class"
            ] = "oarepo_runtime.services.schema.i18n_ui.I18nStrUIField"

        definition_ui_marsh = multilingual_definition_update(definition_ui_marsh, mult_definition)
        deepmerge(definition_ui, {"marshmallow": definition_ui_marsh})
        deepmerge(definition, {"ui": definition_ui})

        def_properties = definition.get("properties", {})
        definition["sample"] = {"skip": False}

        def_properties[lang] = {"type": "keyword", "mapping": {"ignore_above": 256}}
        def_properties[value] = {"type": value_type}
        definition["properties"] = def_properties

        super().prepare(context)
