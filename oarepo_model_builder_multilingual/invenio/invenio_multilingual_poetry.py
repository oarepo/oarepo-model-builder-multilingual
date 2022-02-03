from oarepo_model_builder.builders import OutputBuilder
from oarepo_model_builder.outputs.toml import TOMLOutput

class InvenioMultilingualPoetryBuilder(OutputBuilder):
    TYPE = "invenio_multilingual_poetry"

    def finish(self):
        super().finish()

        output: TOMLOutput = self.builder.get_output("toml", "pyproject.toml")

        output.setdefault(
            "tool.poetry.dependencies.deepmerge",
            "version",
            "^1.0.1",
            "optional",
            True,
            "allow-prereleases",
            True,
        )

        sample_app = output.get("tool.poetry.extras", "sample-app")
        print(sample_app.append('deepmerge'))

        output.set(
            "tool.poetry.extras",
            "sample-app",
            sample_app,
        )
