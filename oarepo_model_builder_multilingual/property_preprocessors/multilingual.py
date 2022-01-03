from oarepo_model_builder_multilingual.model_preprocessors.jsonschema import JSONSchemaBuilder
from oarepo_model_builder_multilingual.model_preprocessors.mapping import MappingBuilder
from oarepo_model_builder_multilingual.invenio.invenio_record_schema import InvenioRecordSchemaBuilder
from oarepo_model_builder_multilingual.property_preprocessors import PropertyPreprocessor, process
from oarepo_model_builder_multilingual.utils.deepmerge import deepmerge
from oarepo_model_builder_multilingual.stack import  ReplaceElement
from deepmerge import always_merger

def titles_gen(supported_langs, key):
    data = {}
    for lan in supported_langs:
        alt = {key + '_' + lan : {
                'type': 'fulltext'
            }}
        always_merger.merge(data, alt)
    return data


class MultilangPreprocessor(PropertyPreprocessor):
    @process(model_builder=JSONSchemaBuilder,
             path='**/properties/*',
             condition=lambda current: current.type == 'multilingual')
    def modify_multilang_schema(self, data, stack, **kwargs):
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
             condition=lambda current: current.type == 'multilingual')
    def modify_multilang_mapping(self, data, stack, **kwargs):
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

        always_merger.merge(data, alternative)

        raise ReplaceElement(data)

    @process(model_builder=InvenioRecordSchemaBuilder,
             path='**/properties/*',
             condition=lambda current: current.type == 'multilingual')
    def modify_multilang_marshmallow(self, data, stack, **kwargs):
        data['type'] = 'object'
        deepmerge(data.setdefault('oarepo:marshmallow', {}), {
            'imports': [{
                'import': 'oarepo_model_builder_multilingual.schema',
                'alias': 'multilingual'
            }],
            'class': 'multilingual.MultilingualSchema',
            'list_nested': True
        })
        return data
