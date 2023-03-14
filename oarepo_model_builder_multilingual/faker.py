import random

from faker import Faker
from oarepo_model_builder.datatypes import datatypes
from oarepo_model_builder.invenio.invenio_script_sample_data import SKIP



def multilingual_sample_provider(faker, settings, stack, params):
    if stack.top.schema_element_type not in ("property", "items"):
        return SKIP
    # d_type = datatypes.get_datatype(
    #     stack.top.data,
    #     stack.top.key,
    #     object.schema.current_model,
    #     object.schema,
    #     stack,
    # )
    # print(d_type)
    if stack.top.data.get("type") == "multilingual":

        def get_faker(lang):
            try:
                return Faker(lang)
            except:
                return Faker()

        return [
            {"lang": lang, "value": get_faker(lang).sentence(nb_words=6)}
            for lang in faker.random_elements(
                elements=settings["supported_langs"].keys(),
                length=min(3, len(settings["supported_langs"].keys())),
                unique=True,
            )
        ]

    elif stack.top.data.get("type") == "i18nStr":

        def get_faker(lang):
            try:
                return Faker(lang)
            except:
                return Faker()

        definition = stack.top.data.get("multilingual", {})
        lang_name = definition.get("lang-field", "lang")
        field_name = definition.get("value-field", "value")
        lang = random.choice(list(settings["supported_langs"].keys()))
        return {lang_name: lang, field_name: get_faker(lang).sentence(nb_words=6)}

    else:
        return SKIP
