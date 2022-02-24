from oarepo_model_builder.builders import process
from oarepo_model_builder.utils.jinja import package_name

from oarepo_model_builder.outputs.json_stack import JSONStack
from oarepo_model_builder.utils.deepmerge import deepmerge
from oarepo_model_builder.utils.hyphen_munch import HyphenMunch
from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder

OAREPO_SORTABLE_PROPERTY = "oarepo:sortable"

class InvenioRecordSearchOptionsBuilderMultilingual(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_search"
    class_config = "record-search-options-class"
    template = None

    def begin(self, schema, settings):
        super().begin(schema, settings)
        self.template = "multi-search"
        self.search_options_data = []
        self.sort_options_data = []
        self.search_facets_definiton = []
        self.search_options_stack = JSONStack()

        self.settings = settings


    def finish(self, **extra_kwargs):
        super().finish(
                       sort_definition = self.sort_options_data)




    @process("/model/**", condition=lambda current, stack: stack.schema_valid)
    def enter_model_element(self):
        schema_element_type = self.stack.top.schema_element_type

        definition = None
        recurse = True

        if recurse:
            # process children
            self.build_children()

        data = self.stack.top.data

        if schema_element_type == "property" and data.type == "multilingual" and OAREPO_SORTABLE_PROPERTY in data:

            for lang in self.settings.supported_langs:

                if 'key' in data[OAREPO_SORTABLE_PROPERTY]:
                    key = data[OAREPO_SORTABLE_PROPERTY]['key'] + '_' + lang
                else:
                    key = self.process_name(self.stack.path, type="name") + '_' + lang
                field = self.process_name(self.stack.path, type="field") + '_' + lang
                order = data[OAREPO_SORTABLE_PROPERTY].get('order', 'asc')
                if order == "desc":
                    field = "-" + field
                self.sort_options_data.append({key: dict(fields = [field])})

    def process_name(self, path, type):
        path_array = (path.split("/"))[3:]
        name = path_array[0]
        if len(path_array) == 1:
            return name
        path_array.pop(0)

        for path in path_array:
            if path == "properties":
                continue
            if type == "name":
                name = name + "_" + path
            elif type == "field":
                name = name + "." + path

        return name
