import random

from oarepo_model_builder.invenio.invenio_script_sample_data import SKIP


def multilingual_sample_provider(faker, settings, stack, params):
    if stack.top.schema_element_type not in ("property", "items"):
        return SKIP

    try:
        type = stack[-3].json_schema_type
    except:
        type = None
    if type == "i18nStr":
        definition = stack.top.data.get("multilingual", {})
        lang_name = definition.get("lang-field", "lang")
        if stack.top.key == lang_name:
            return random.choice(list(settings["supported_langs"].keys()))

    return SKIP
