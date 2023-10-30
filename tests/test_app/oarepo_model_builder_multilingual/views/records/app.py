from flask import Blueprint


def create_app_blueprint(app):
    blueprint = Blueprint(
        "oarepo_model_builder_multilingual_app",
        __name__,
        url_prefix="/oarepo-model-builder-multilingual/",
    )
    blueprint.record_once(init_create_app_blueprint)

    # calls record_once for all other functions starting with "init_addons_"
    # https://stackoverflow.com/questions/58785162/how-can-i-call-function-with-string-value-that-equals-to-function-name
    funcs = globals()
    funcs = [
        v
        for k, v in funcs.items()
        if k.startswith("init_addons_oarepo_model_builder_multilingual") and callable(v)
    ]
    for func in funcs:
        blueprint.record_once(func)

    return blueprint


def init_create_app_blueprint(state):
    """Init app."""
    app = state.app
    ext = app.extensions["oarepo_model_builder_multilingual"]

    # register service
    sregistry = app.extensions["invenio-records-resources"].registry
    sregistry.register(
        ext.service_records, service_id=ext.service_records.config.service_id
    )

    # Register indexer
    if hasattr(ext.service_records, "indexer"):
        iregistry = app.extensions["invenio-indexer"].registry
        iregistry.register(
            ext.service_records.indexer,
            indexer_id=ext.service_records.config.service_id,
        )
