from oarepo_model_builder.utils.deepmerge import deepmerge


def alternative_gen(supported_langs, key):
    data = {}
    for lan in supported_langs:
        alt = {
            key
            + "_"
            + lan: {
                "type": "text",
            }
        }
        multilang_options = {}

        if "text" in supported_langs[lan]:
            deepmerge(multilang_options, supported_langs[lan]["text"])
        fields_dict = {}
        if "sort" in supported_langs[lan]:
            sort = deepmerge(
                supported_langs[lan]["sort"], {"index": False, "language": lan}
            )
            deepmerge(fields_dict, {"sort": sort})

        deepmerge(fields_dict, {"keyword": {"type": "keyword", "ignore_above": 256}})
        if fields_dict != {}:
            deepmerge(multilang_options, {"fields": fields_dict})

        option = deepmerge(
            {"type": "text"},
            multilang_options,
            [],
        )

        data = deepmerge(data, {str(key + "_" + lan): option})

    return data
