import munch
from oarepo_model_builder.builders import process
from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder
from oarepo_model_builder.outputs.json_stack import JSONStack
from oarepo_model_builder.utils.deepmerge import deepmerge
from oarepo_model_builder.utils.hyphen_munch import HyphenMunch
from oarepo_model_builder.utils.jinja import package_name


class InvenioRecordMultilingualDumperBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_dumper"
    class_config = "multilingual-dumper-class"
    template = "multilingual-record-dumper"

    def begin(self, schema, settings):
        super().begin(schema, settings)
        self.paths = []
        self.langs = []

    def finish(self, **extra_kwargs):
        for lang in self.settings["supported-langs"]:
            self.langs.append(lang)

        super().finish(langs=self.langs, paths=self.paths)
        python_path = self.class_to_path(self.current_model["record-class"])
        self.process_template(
            python_path,
            "record-multilingual",
            current_package_name=package_name(self.current_model["record-class"]),
            **extra_kwargs,
        )

    @process("/**", condition=lambda current, stack: stack.schema_valid)
    def enter_model_element(self):
        definition = None
        recurse = True


        if recurse:
            # process children
            self.build_children()
        try:
            type = self.stack[-3].json_schema_type
        except:
            type = None
        path_stack = []
        if type == "i18nStr":
            for s in self.stack:
                type = s.schema_element_type
                if type and type == "property": #skip items
                    path_stack.append(s.key)

            path_stack.pop()
            path = ""
            for p in path_stack:
                path += '/'+ p
            if path not in self.paths:
                self.paths.append(path)
