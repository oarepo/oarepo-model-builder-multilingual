from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder
from oarepo_model_builder.builders import process
from oarepo_model_builder.stack import ModelBuilderStack
from oarepo_model_builder.outputs.json_stack import JSONStack
from oarepo_model_builder.utils.schema import is_schema_element
from oarepo_model_builder.utils.jinja import package_name

paths = []

class InvenioRecordMultilingualDumperBuilder(InvenioBaseClassPythonBuilder):
    TYPE = 'invenio_record_dumper'
    class_config = 'multilingual-dumper-class'
    template = 'multilingual-record-dumper'


    def begin(self, schema, settings):
        super().begin(schema, settings)
        self.stack = JSONStack()


    def finish(self, **extra_kwargs):

        super().finish(
            langs = self.settings.supported_langs,
            paths = paths

        )
        python_path = self.class_to_path(self.settings.python['record-class'])
        self.process_template(python_path, "record-multilingual",
                              current_package_name=package_name(self.settings.python['record-class']),
                              **extra_kwargs)
    @process('/model/**', condition=lambda current, stack: is_schema_element(stack))
    def enter_model_element(self, stack: ModelBuilderStack):

        self.model_element_enter(stack)
        yield

        data = stack.top.data
        if isinstance(data, dict):

            if 'type' in data and 'multilingual' in data['type']:
                path = stack.path.replace('/model/properties', '/metadata')
                paths.append(path)


        self.model_element_leave(stack)

    def model_element_leave(self, stack: ModelBuilderStack):
        self.stack.pop()
    def model_element_enter(self, stack: ModelBuilderStack):
        top = stack.top
        match stack.top_type:
            case stack.PRIMITIVE:
                self.stack.push(top.key, top.data)
            case stack.LIST:
                self.stack.push(top.key, [])
            case stack.DICT:
                self.stack.push(top.key, {})

