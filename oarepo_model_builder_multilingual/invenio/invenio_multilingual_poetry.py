from oarepo_model_builder.builders import OutputBuilder
from oarepo_model_builder.outputs.toml import TOMLOutput


class InvenioMultilingualPoetryBuilder(OutputBuilder):
    TYPE = "invenio_multilingual_poetry"

    def finish(self):
        super().finish()

        output: TOMLOutput = self.builder.get_output("toml", "pyproject.toml")

        output.setdefault("tool.poetry.dependencies.deepmerge", "version", "^1.0.1")

        output.setdefault(
            "tool.poetry.dependencies.langcodes",
            "version",
            "^3.3.0",
        )
