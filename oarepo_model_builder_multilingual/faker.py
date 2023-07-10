import random

from oarepo_model_builder.invenio.invenio_script_sample_data import SKIP


def multilingual_sample_provider(faker, settings, stack, params):
    try:
        type = stack.stack[-3].model_type
        if type != "i18nStr" and type != "multilingual":
            type = stack.stack[-2].model_type
    except:
        type = None
    if type == "i18nStr" or type == "multilingual":
        if hasattr(stack.stack[-1], "multilingual"):
            definition = stack.stack[-1]["multilingual"]
        else:
            definition = {}
        lang_name = definition.get("lang-field", "lang")
        if stack.key == lang_name:
            return random.choice(list(settings["supported-langs"].keys()))

    return SKIP
