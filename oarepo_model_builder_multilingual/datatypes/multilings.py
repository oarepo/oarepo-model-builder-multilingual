import copy

from marshmallow import fields
from oarepo_model_builder.datatypes import DataType
from oarepo_model_builder.datatypes.containers import ObjectDataType, ArrayDataType, NestedDataType
from oarepo_model_builder.stack import ReplaceElement
from oarepo_model_builder.utils.deepmerge import deepmerge
from oarepo_model_builder.utils.facet_helpers import facet_definiton, facet_name
from oarepo_model_builder.validation import model_validator
from oarepo_model_builder.validation.property_marshmallow import ObjectPropertyMarshmallowSchema
from oarepo_model_builder.validation.ui import ObjectPropertyUISchema

from oarepo_model_builder_multilingual.utils.supported_langs import alternative_gen


class MultilingualDataType(ArrayDataType):
    schema_type = "property"
    mapping_type = "multilingual"
    marshmallow_field = "ma_fields.List"
    model_type = "multilingual"

    class ModelSchema(DataType.ModelSchema):
        pass

    def prepare(self, context):
        definition = self.definition
        definition['type'] = 'array'
        definition['items'] = {'type': "i18nStr"}

        super().prepare(context)


class I18nDataType(NestedDataType):
    schema_type = "object" #todo facets problem
    mapping_type = "i18nStr"
    marshmallow_field = "ma_fields.Nested"
    model_type = "i18nStr"
    json_schema_type = "nested"

    class ModelSchema(ObjectPropertyMarshmallowSchema,
                      ObjectPropertyUISchema,
                      NestedDataType.ModelSchema,
                      ):
        pass

    def prepare(self, context):
        definition = self.definition
        mult_definition = definition.get('multilingual', {})

        lang = mult_definition.get('lang-field', 'lang')
        value = mult_definition.get('value-field', 'value')
        definition['type'] = 'i18nStr'


        if 'lang-field' not in mult_definition and 'value-field' not in mult_definition and 'properties' not in definition:
            definition_marshmallow = definition.get('marshmallow', {})
            definition_marshmallow['generate'] = False
            definition_marshmallow['schema-class'] = 'oarepo_runtime.i18n.schema.I18nSchema'
            definition_marshmallow['imports'] = [{'import': 'oarepo_runtime.i18n.schema.I18nSchema'}]

            definition['marshmallow'] = definition_marshmallow
            definition_ui = definition.get('ui', {})
            definition_ui['detail'] = 'multilingual'
            definition_ui['marshmallow'] = {'generate': False,
                                            'schema-class': 'oarepo_runtime.i18n.schema.I18nUISchema',
                                            'imports': [{'import': 'oarepo_runtime.i18n.schema.I18nUISchema'}]}

            definition['ui'] = definition_ui
        def_properties = definition.get('properties', {})
        definition['sample'] = {'skip': False}

        def_properties[lang] = {'type': 'keyword'} #, 'sample': {'skip': True}
        def_properties[value] = {'type': 'fulltext+keyword'} #, 'sample': {'skip': True}
        definition['properties'] = def_properties

        super().prepare(context)


    def marshmallow(self, **extras):
        ret = copy.deepcopy(self.definition.get("marshmallow", {}))
        if not 'class' in ret:
            ret.setdefault("field-class", self.marshmallow_field)
        ret.setdefault("validators", []).extend(self.marshmallow_validators())
        deepmerge(ret.setdefault("validates", {}),

                  { "validates": {
                            "lang": {
                                "imports": ["import langcodes"],
                                "definition": """def validate_lang(self, value):
                                        if value != "_" and not langcodes.Language.get(value).is_valid():
                                            raise ma_ValidationError("Invalid language code")""",
                            }
                        }}

                )
        for k, v in extras.items():
            if v is not None:
                ret[k] = v
        return ret

    # # todo multilang facets
    # def get_facet(self, stack, parent_path):
    #     key, field = facet_definiton(self)
    #     path = parent_path
    #     if len(parent_path) > 0 and self.key:
    #         path = parent_path + '.' + self.key
    #     elif self.key:
    #         path = self.key
    #     if field:
    #         return field, facet_name(path)
    #     else:
    #         return f"TermsFacet(field=\"{path}\")", facet_name(path)
