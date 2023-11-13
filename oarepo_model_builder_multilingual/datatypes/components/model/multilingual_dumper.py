import marshmallow as ma
from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.datatypes.components import RecordDumperModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default
from oarepo_model_builder.utils.python_name import parent_module
from oarepo_model_builder.validation.utils import ImportSchema


class MultilingualDumperClassSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    generate = ma.fields.Bool(metadata={"doc": "Generate the dumper class"})
    class_ = ma.fields.Str(
        attribute="class",
        data_key="class",
        metadata={"doc": "Qualified name of the class"},
    )
    base_classes = ma.fields.List(
        ma.fields.Str(),
        attribute="base-classes",
        data_key="base-classes",
        metadata={"doc": "List of base classes"},
    )
    extensions = ma.fields.List(
        ma.fields.Str(), metadata={"doc": "List of dumper extensions"}
    )
    extra_code = ma.fields.Str(
        attribute="extra-code",
        data_key="extra-code",
        metadata={"doc": "Extra code to be copied to the bottom of the dumper file"},
    )
    module = ma.fields.String(metadata={"doc": "Class module"})
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "List of python imports"}
    )


class MultilingualDumperModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [RecordDumperModelComponent]

    class ModelSchema(ma.Schema):
        multilingual_record_dumper = ma.fields.Nested(
            MultilingualDumperClassSchema,
            attribute="multilingual-dumper",
            data_key="multilingual-dumper",
            metadata={"doc": "Settings for record dumper"},
        )

    def before_model_prepare(self, datatype, *, context, **kwargs):
        multilingual_record_module = parent_module(
            datatype.definition["record"]["module"]
        )

        multilingual_dumper = set_default(datatype, "multilingual-dumper", {})
        multilingual_dumper.setdefault("generate", True)

        multilingual_dumper_module = multilingual_dumper.setdefault(
            "module", f"{multilingual_record_module}.dumpers.multilingual"
        )
        multilingual_dumper.setdefault(
            "class", f"{multilingual_dumper_module}.MultilingualSearchDumperExt"
        )
        multilingual_dumper.setdefault(
            "base-classes",
            ["oarepo_runtime.records.dumpers.multilingual_dumper.MultilingualDumper"],
        )
        multilingual_dumper.setdefault("extra-code", "")
        multilingual_dumper.setdefault("extensions", [])
        multilingual_dumper.setdefault("imports", [])
        dumper = set_default(datatype, "record-dumper", {})
        dumper.setdefault("generate", True)
        extensions = dumper.setdefault("extensions", [])
        extensions.append(
            f"{{{{{multilingual_dumper_module}.MultilingualSearchDumperExt}}}}()"
        )
