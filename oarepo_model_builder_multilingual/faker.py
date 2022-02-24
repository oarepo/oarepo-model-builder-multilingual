from faker import Faker
from oarepo_model_builder.invenio.invenio_script_sample_data import SKIP


def multilingual_sample_provider(faker, settings, stack, params):
    if stack.top.schema_element_type not in ('property', 'items'):
        return SKIP
    if stack.top.data.get('type') != 'multilingual':
        return SKIP

    def get_faker(lang):
        try:
            return Faker(lang)
        except:
            return Faker()

    return [
        {
            'lang': lang,
            'value': get_faker(lang).sentence(nb_words=6)
        }
        for lang in faker.random_elements(elements=settings['supported_langs'].keys(),
                                          length=min(3, len(settings['supported_langs'].keys())),
                                          unique=True)
    ]
