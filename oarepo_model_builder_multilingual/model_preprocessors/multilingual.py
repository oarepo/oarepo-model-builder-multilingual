from oarepo_model_builder.model_preprocessors import ModelPreprocessor

class MultilingualModelPreprocessor(ModelPreprocessor):
    def transform(self, schema, settings):
        self.set(settings.python, 'multilingual-dumper-class',
                 lambda: f'{settings.package}.services.multilingual_dumper.MultilingualDumper')