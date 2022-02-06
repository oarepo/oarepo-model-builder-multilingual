from oarepo_model_builder.model_preprocessors import ModelPreprocessor

class MultilingualModelPreprocessor(ModelPreprocessor):
    def transform(self, schema, settings):
        self.set(settings.python, 'multilingual-dumper-class',
                 lambda: f'{settings.python.record_records_package}.multilingual_dumper.MultilingualDumper')
        self.set(settings.python, 'multilingual-schema-class',
                 lambda: f'{settings.python.record_services_package}.multilingual_schema.MultilingualSchema')