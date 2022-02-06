from oarepo_model_builder.builders.jsonschema import JSONSchemaBuilder
from oarepo_model_builder.builders.mapping import MappingBuilder
from oarepo_model_builder.invenio.invenio_record_schema import InvenioRecordSchemaBuilder
from oarepo_model_builder.invenio.invenio_script_sample_data import InvenioScriptSampleDataBuilder
from oarepo_model_builder.property_preprocessors import PropertyPreprocessor, process
from oarepo_model_builder.stack import ReplaceElement, ModelBuilderStack
from oarepo_model_builder.utils.deepmerge import deepmerge


def titles_gen(supported_langs, key):
    data = {}
    for lan in supported_langs:
        alt = {key + '_' + lan: {
            'type': 'fulltext+keyword'
        }}
        data = deepmerge(data, alt)
    return data


class MultilangPreprocessor(PropertyPreprocessor):

    @process(model_builder=JSONSchemaBuilder,
             path='**/properties/*',
             condition=lambda current, stack: current.type == 'multilingual')
    def modify_multilang_schema(self, data, stack: ModelBuilderStack, **kwargs):
        data['type'] = 'array'
        data['items'] = {
            "type": 'object',
            "properties": {
                'lang': {
                    'type': 'string'
                },
                'value': {
                    'type': 'string'
                }
            }
        }
        return data

    @process(model_builder=MappingBuilder,
             path='**/properties/*',
             condition=lambda current, stack: current.type == 'multilingual')
    def modify_multilang_mapping(self, data, stack: ModelBuilderStack, **kwargs):
        alternative = titles_gen(self.settings.supported_langs, stack.top.key)

        data = {
            stack.top.key: {
                'type': 'object',
                'properties': {
                    'lang': {
                        'type': 'keyword'
                    },
                    'value': {
                        'type': 'fulltext'
                    }
                }
            }
        }

        deepmerge(data, alternative)

        raise ReplaceElement(data)

    @process(model_builder=InvenioRecordSchemaBuilder,
             path='**/properties/*',
             condition=lambda current, stack: current.type == 'multilingual')
    def modify_multilang_marshmallow(self, data, stack: ModelBuilderStack, **kwargs):
        data['type'] = 'object'
        deepmerge(data.setdefault('oarepo:marshmallow', {}), {
            'class': self.settings.python.multilingual_schema_class,
            'list_nested': True
        })
        return data
