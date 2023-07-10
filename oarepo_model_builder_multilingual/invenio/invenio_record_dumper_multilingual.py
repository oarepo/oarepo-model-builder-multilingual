from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordMultilingualDumperBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_multilingual_dumper"
    section = "multilingual-dumper"
    template = "multilingual-record-dumper"
    paths = []

    def finish(self, **extra_kwargs):
        langs = []
        for lang in self.settings["supported-langs"]:
            langs.append(lang)

        self.get_paths(self.current_model.children)
        extra_kwargs["langs"] = langs
        extra_kwargs["paths"] = sorted(set(self.paths))
        super().finish(**extra_kwargs)

    def get_paths(self, parent_node):
        children = parent_node
        for c in children:
            node = children[c]
            if node.model_type == "i18nStr" or node.model_type == "multilingual":
                self.paths.append(self.process_paths(node.path))
            elif node.children != {}:
                self.get_paths(node.children)
            elif hasattr(node, "item"):
                self.get_paths({"item": node.item})

    def process_paths(self, path):
        components = path.split(".")
        return "/" + "/".join(components)
