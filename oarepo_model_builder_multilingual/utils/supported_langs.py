from oarepo_model_builder.utils.deepmerge import deepmerge


def alternative_gen(supported_langs, key):
    data = {}
    for lan in supported_langs:
        alt = {
            key
            + "_"
            + lan: {
                "type": "fulltext+keyword",
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

        if "keyword" in supported_langs[lan]:
            deepmerge(
                fields_dict,
                {"keyword": supported_langs[lan]["keyword"]},
            )
        if fields_dict != {}:
            deepmerge(multilang_options, {"fields": fields_dict})
        deepmerge(
            alt[key + "_" + lan].setdefault("mapping", {}),
            multilang_options,
            [],
        )

        data = deepmerge(data, alt)

    return data
