from pkg_resources import parse_version

from oarepo_model_builder.builders import OutputBuilder
from oarepo_model_builder.outputs.cfg import CFGOutput
from oarepo_model_builder.utils.verbose import log


class MultSetupCfgBuilder(OutputBuilder):
    TYPE = "setup_cfg"

    def finish(self):
        super().finish()
        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")
        output.add_dependency("deepmerge", ">=1.1.0")