import copy

from oarepo_model_builder.datatypes import DataType
from oarepo_model_builder.datatypes.containers import ArrayDataType, NestedDataType
from oarepo_model_builder.utils.deepmerge import deepmerge
from oarepo_model_builder.validation.property_marshmallow import (
    ObjectPropertyMarshmallowSchema,
)
from oarepo_model_builder.validation.ui import ObjectPropertyUISchema
from oarepo_model_builder.utils.facet_helpers import facet_name


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

        super().prepare(context)


class I18nDataType(NestedDataType):
    schema_type = "object"
    mapping_type = "i18nStr"
    marshmallow_field = "ma_fields.Nested"
    model_type = "i18nStr"
    json_schema_type = "nested"

    class ModelSchema(
        ObjectPropertyMarshmallowSchema,
        ObjectPropertyUISchema,
        NestedDataType.ModelSchema,
    ):
        pass

    def prepare(self, context):
        definition = self.definition
        mult_definition = definition.get("multilingual", {})

        lang = mult_definition.get("lang-field", "lang")
        value = mult_definition.get("value-field", "value")
        definition["type"] = "i18nStr"

        if (
            "lang-field" not in mult_definition
            and "value-field" not in mult_definition
            and "properties" not in definition
        ):
            definition_marshmallow = definition.get("marshmallow", {})
            definition_marshmallow["generate"] = False
            definition_marshmallow[
                "schema-class"
            ] = "oarepo_runtime.i18n.schema.I18nSchema"
            definition_marshmallow["imports"] = [
                {"import": "oarepo_runtime.i18n.schema.I18nSchema"}
            ]

            definition["marshmallow"] = definition_marshmallow
            definition_ui = definition.get("ui", {})
            definition_ui["detail"] = "multilingual"
            definition_ui["marshmallow"] = {
                "generate": False,
                "schema-class": "oarepo_runtime.i18n.schema.I18nUISchema",
                "imports": [{"import": "oarepo_runtime.i18n.schema.I18nUISchema"}],
            }

            definition["ui"] = definition_ui
        def_properties = definition.get("properties", {})
        definition["sample"] = {"skip": False}

        def_properties[lang] = {"type": "keyword"}
        def_properties[value] = {"type": "fulltext+keyword"}
        definition["properties"] = def_properties

        super().prepare(context)

    def marshmallow(self, **extras):
        ret = copy.deepcopy(self.definition.get("marshmallow", {}))
        if not "class" in ret:
            ret.setdefault("field-class", self.marshmallow_field)
        ret.setdefault("validators", []).extend(self.marshmallow_validators())
        deepmerge(
            ret.setdefault("validates", {}),
            {
                "validates": {
                    "lang": {
                        "imports": ["import langcodes"],
                        "definition": """def validate_lang(self, value):
                                        if value != "_" and not langcodes.Language.get(value).is_valid():
                                            raise ma_ValidationError("Invalid language code")""",
                    }
                }
            },
        )
        for k, v in extras.items():
            if v is not None:
                ret[k] = v
        return ret

    def get_facet(self, stack, parent_path):
        if not stack:
            return None
        path = parent_path
        if len(parent_path) > 0 and self.key:
            path = parent_path + "." + self.key
        elif self.key:
            path = self.key
        facet_obj = stack[0].get_facet(stack[1:], path)
        lang_name = "lang"
        try:
            i18n_data = self.stack.stack[-3].data
            if "multilingual" in i18n_data:
                lang_name = i18n_data["multilingual"].get("lang-field", "lang")
        except:
            pass
        nested_arr = []
        for f in facet_obj:
            nested_arr.append(
                {
                    "facet": f'NestedLabeledFacet(path ="{path}", nested_facet = {f["facet"]})',
                    "path": f["path"],
                }
            )
        if self.stack.top.key == lang_name:
            for lang in self.schema.settings["supported-langs"]:
                l_path = path + "_" + lang
                nested_arr.append(
                    {
                        "facet": f'TermsFacet(field="{l_path}")',
                        "path": facet_name(l_path),
                    }
                )
        return nested_arr
