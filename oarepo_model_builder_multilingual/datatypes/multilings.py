import copy

from marshmallow import fields
from oarepo_model_builder.datatypes import DataType
from oarepo_model_builder.datatypes.containers import ObjectDataType, ArrayDataType
from oarepo_model_builder.stack import ReplaceElement
from oarepo_model_builder.utils.deepmerge import deepmerge
from oarepo_model_builder.utils.facet_helpers import facet_definiton, facet_name
from oarepo_model_builder.validation import model_validator

from oarepo_model_builder_multilingual.utils.supported_langs import alternative_gen


class MultilingualDataType(ArrayDataType):
    schema_type = "property"
    mapping_type = "multilingual"
    marshmallow_field = "ma_fields.List"
    model_type = "multilingual"

    class ModelSchema(DataType.ModelSchema):
        pass

    def mapping(self, **extras):
        alternative = alternative_gen(self.schema.settings["supported-langs"], self.key)
        data = {
            self.key: {
                "type": "object",
                "properties": {
                    "lang": {"type": "keyword"},
                    "value": {"type": "fulltext"},
                },
            }
        }

        deepmerge(data, alternative)

        raise ReplaceElement(data)

    def json_schema(self, **extras):
        data = super().json_schema()
        data["type"] = "array"
        data["items"] = {
            "type": "object",
            "properties": {"lang": {"type": "string"}, "value": {"type": "string"}},
        }
        return data


    #todo multilang facets
    def get_facet(self, stack, parent_path):
        key, field = facet_definiton(self)
        path = parent_path
        if len(parent_path) > 0 and self.key:
            path = parent_path + '.' + self.key + '.lang'
        elif self.key:
            path = self.key + '.lang'
        if field:
            return field, facet_name(path)
        else:
            return f"TermsFacet(field=\"{path}\")", facet_name(path)


class I18nDataType(ObjectDataType):
    schema_type = "property" #todo facety problem
    mapping_type = "i18nStr"
    marshmallow_field = "ma_fields.Nested"
    model_type = "i18nStr"
    json_schema_type = "object"


    class ModelSchema(DataType.ModelSchema):
        properties = fields.Nested(
            lambda: model_validator.validator_class("properties", strict=False)()
        )

    def mapping(self, **extras):
        alternative = alternative_gen(self.schema.settings["supported-langs"], self.key)
        definition = self.definition.get("multilingual", {})

        lang = definition.get("lang-field", "lang")
        value = definition.get("value-field", "value")
        properties = self.definition.get("properties", {})

        data = {
            self.key: {
                "type": "object",
                "properties": {
                    lang: {"type": "keyword"},
                    value: {"type": "fulltext"},
                    **properties,
                },
            }
        }

        deepmerge(data, alternative)

        raise ReplaceElement(data)

    def json_schema(self, **extras):
        data = super().json_schema()
        data["type"] = "object"
        definition = data.get("multilingual", {})

        lang = definition.get("lang-field", "lang")
        value = definition.get("value-field", "value")
        properties = data.get("properties", {})

        data["properties"] = {
            lang: {"type": "string", "required": True},
            value: {"type": "string", "required": True},
            **properties,
        }
        return data

    # def marshmallow(self, **extras):
    #     ret = copy.deepcopy(self.definition.get("marshmallow", {}))
    #     if not 'class' in ret:
    #         ret.setdefault("field-class", self.marshmallow_field)
    #     ret.setdefault("validators", []).extend(self.marshmallow_validators())
    #     for k, v in extras.items():
    #         if v is not None:
    #             ret[k] = v
    #     return ret
    #todo multilang facets
    def get_facet(self, stack, parent_path):
        key, field = facet_definiton(self)
        path = parent_path
        if len(parent_path) > 0 and self.key:
            path = parent_path + '.' + self.key
        elif self.key:
            path = self.key
        if field:
            return field, facet_name(path)
        else:
            return f"TermsFacet(field=\"{path}\")", facet_name(path)
