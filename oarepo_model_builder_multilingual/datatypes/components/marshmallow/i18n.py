from typing import List

from oarepo_model_builder.datatypes import DataType, Import, datatypes
from oarepo_model_builder.datatypes.components import (
    ObjectMarshmallowComponent,
    RegularMarshmallowComponent,
)
from oarepo_model_builder.datatypes.components.marshmallow import MarshmallowField
from oarepo_model_builder.datatypes.components.marshmallow.graph import MarshmallowClass
from oarepo_model_builder.utils.absolute_class import convert_to_absolute_class_name
from oarepo_model_builder.utils.python_name import qualified_name

from oarepo_model_builder_multilingual.datatypes import I18nDataType


class I18nMarshmallowMixin:
    def _register_class_name(
        self, datatype, marshmallow_config, classes, marshmallow_module
    ):
        schema_class = marshmallow_config.get("class")
        if not schema_class:
            return
        schema_class = convert_to_absolute_class_name(schema_class, marshmallow_module)
        classes[schema_class].append(
            (datatype, marshmallow_config.get("generate", True))
        )

    def _build_class_name(
        self,
        datatype,
        marshmallow_config,
        definition_marshmallow,
        classes,
        marshmallow_module,
        fingerprint,
        suffix,
    ):
        schema_class = marshmallow_config.get("class")
        generate = marshmallow_config.get("generate", True)

        if schema_class:
            qualified_schema_class = qualified_name(marshmallow_module, schema_class)
            if qualified_schema_class != schema_class:
                marshmallow_config["class"] = qualified_schema_class
                definition_marshmallow["class"] = qualified_schema_class
                schema_class = qualified_schema_class
            if not generate:
                if fingerprint not in classes:
                    classes[fingerprint] = schema_class
                return

    def _build_class(
        self, datatype, marshmallow, children, field_generator, classes  # NOSONAR
    ):
        fields = []
        for _, c in sorted(children.items()):
            datatypes.call_components(c, field_generator, fields=fields)
        extra_fields = [
            MarshmallowField(f["name"], f["value"])
            for f in marshmallow.get("extra-fields", [])
        ]
        fields = [*fields, *extra_fields]
        fields.sort(key=lambda x: (not x.key.startswith("_"), x.key))
        classes.append(
            MarshmallowClass(
                class_name=marshmallow["class"],
                base_classes=marshmallow.get("base-classes", []) or ["ma.Schema"],
                imports=Import.from_config(marshmallow.get("imports", [])),
                fields=fields,
                strict=True,
            )
        )


class I18nMarshmallowComponent(I18nMarshmallowMixin, ObjectMarshmallowComponent):
    eligible_datatypes = [I18nDataType]

    def marshmallow_field(
        self, datatype: DataType, *, fields: List[MarshmallowField], **kwargs
    ):
        f = []

        RegularMarshmallowComponent.marshmallow_field(self, datatype=datatype, fields=f)
        if not f:
            # the marshmallow field was not generated (read=False & write=False)
            return

        fld: MarshmallowField = f[0]
        fields.append(fld)

    def marshmallow_build_class(self, *, datatype, classes, **kwargs):
        self._build_class(
            datatype,
            datatype.section_marshmallow.config,
            datatype.section_marshmallow.children,
            "marshmallow_field",
            classes,
        )

    def _marshmallow_field_arguments(self, datatype, section, marshmallow, field_name):
        return [
            *RegularMarshmallowComponent._marshmallow_field_arguments(
                self, datatype, section, marshmallow, field_name
            ),
        ]
