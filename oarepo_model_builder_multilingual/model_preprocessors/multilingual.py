from oarepo_model_builder.model_preprocessors import ModelPreprocessor


class MultilingualModelPreprocessor(ModelPreprocessor):
    def transform(self, schema, settings):
        model = schema.current_model
        self.set(
            model,
            "multilingual-dumper-class",
            lambda: f"{model.record_records_package}.multilingual_dumper.MultilingualDumper",
        )
        self.set(
            model,
            "multilingual-schema-class",
            lambda: f"{model.record_services_package}.multilingual_schema.MultilingualSchema",
        )
        self.set(
            model,
            "i18n-schema-class",
            lambda: f"{model.record_services_package}.i18nStr_schema.i18nStrSchema",
        )
        self.set(
            model,
            "multilingual-ui-schema-class",
            lambda: f"{model.record_services_package}.multilingual_schema.MultilingualUISchema",
        )
        self.set(
            model,
            "i18n-ui-schema-class",
            lambda: f"{model.record_services_package}.i18nStr_schema.i18nStrUISchema",
        )
