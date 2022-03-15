from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
from oarepo_model_builder.builders.mapping import MappingBuilder
from oarepo_model_builder.invenio.invenio_record_schema import InvenioRecordSchemaBuilder
from oarepo_model_builder.property_preprocessors import PropertyPreprocessor, process
from oarepo_model_builder.stack import ReplaceElement, ModelBuilderStack
from oarepo_model_builder.utils.camelcase import camel_case
from oarepo_model_builder.utils.deepmerge import deepmerge


def alternative_gen(supported_langs, key):
    data = {}
    for lan in supported_langs:
        alt = {key + '_' + lan: {
            'type': 'fulltext+keyword',
        }}
        multilang_options = {}

        if 'text' in supported_langs[lan]:
            deepmerge(multilang_options, supported_langs[lan]['text'])

        if 'sort' in supported_langs[lan]:
            sort = deepmerge(supported_langs[lan]['sort'], {'index': False, 'language': lan})
            deepmerge(multilang_options, {'sort': sort})

        if 'keyword' in supported_langs[lan]:
            deepmerge(multilang_options, {'fields': {'keyword': supported_langs[lan]['keyword']}})
        deepmerge(
            alt[key + '_' + lan].setdefault("oarepo:mapping", {}),
            multilang_options,
            [],
        )

        data = deepmerge(data, alt)

    return data


class I18nStrPreprocessor(PropertyPreprocessor):

    @process(model_builder=JSONSchemaBuilder,
             path='**/properties/*',
             condition=lambda current, stack: current.type == 'i18nStr')
    def modify_multilang_schema(self, data, stack: ModelBuilderStack, **kwargs):
        data['type'] = 'object'
        definition = data.get('oarepo:multilingual', {})

        properties = data.get('properties', {})
        lang = definition.get('lang-field', 'lang')
        value = definition.get('value-field', 'value')
        properties = data.get('properties', {})
        data['properties'] = {

                lang: {
                    'type': 'string',
                    'required': True
                },
                value: {
                    'type': 'string',
                    'required': True
                }, **properties

        }
        return data

    @process(model_builder=MappingBuilder,
             path='**/properties/*',
             condition=lambda current, stack: current.type == 'i18nStr')
    def modify_multilang_mapping(self, data, stack: ModelBuilderStack, **kwargs):
        alternative = alternative_gen(self.settings['supported-langs'], stack.top.key)
        definition = data.get('oarepo:multilingual', {})

        lang = definition.get('lang-field', 'lang')
        value = definition.get('value-field', 'value')
        properties = data.get('properties', {})

        data = {
            stack.top.key: {
                'type': 'object',
                'properties': {
                    lang: {
                        'type': 'keyword'

                    },
                    value: {
                        'type': 'fulltext'
                    }, **properties
                }
            }
        }

        deepmerge(data, alternative)

        raise ReplaceElement(data)

    @process(model_builder=InvenioRecordSchemaBuilder,
             path='**/properties/*',
             condition=lambda current, stack: current.type == 'i18nStr')
    def modify_multilang_marshmallow(self, data, stack: ModelBuilderStack, **kwargs):
        definition = data.get('oarepo:multilingual', {})
        use_i18n = False
        if 'usei18n' in definition:
            use_i18n = True
        lang = definition.get('lang-field', 'lang')
        value = definition.get('value-field', 'value')
        properties = data.get('properties', {})
        if lang == 'lang' and value == 'value' and not use_i18n:
            data['type'] = 'object'
            deepmerge(data.setdefault('oarepo:marshmallow', {}), {
                'class': self.settings.python.i18n_schema_class,
                'nested': True
            })
        else:
            data['type'] = 'object'
            data['properties'] = {

                lang: {
                    'type': 'string',
                    'required': True
                },
                value: {
                    'type': 'string',
                    'required': True
                }, **properties

            }
            if 'oarepo:marshmallow' in data and 'class' in data['oarepo:multilingual']:
                class_name = data['oarepo:marshmallow']['class']
            else:
                class_name = camel_case(stack.top.key) + 'Schema'
            deepmerge(data.setdefault('oarepo:marshmallow', {}), {
                'generate': True,
                'class': class_name,
                'nested': True,
                'validates': {lang: { 'imports' : ['import langcodes'],'definition' :'''def validate_lang(self, value):
                                    if value != "_" and not langcodes.Language.get(value).is_valid():
                                        raise ma_ValidationError("Invalid language code")'''}}
            })

        return data
