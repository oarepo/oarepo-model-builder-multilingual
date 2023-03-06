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

    @process("/model/**", condition=lambda current, stack: stack.schema_valid)
    def enter_model_element(self):
        definition = None
        recurse = True

        if recurse:
            # process children
            self.build_children()
        data = self.stack.top.data
        if isinstance(data, dict):
            if "type" in data and "multilingual" in data["type"]:
                path = self.stack.path.replace("/model/properties", "")
                self.paths.append(path)
