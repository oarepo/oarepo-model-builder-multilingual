from oarepo_model_builder.datatypes import datatypes
from oarepo_model_builder.datatypes.components import (
    NestedFacetsComponent,
    RegularFacetsComponent,
)
from oarepo_model_builder.datatypes.components.facets import FacetDefinition
from oarepo_model_builder.utils.facet_helpers import facet_name, flatten

from oarepo_model_builder_multilingual.datatypes import I18nDataType


class I18nStrFacetsComponent(NestedFacetsComponent, RegularFacetsComponent):
    eligible_datatypes = [I18nDataType]

    def process_facets(self, datatype, section, **__kwargs):
        facet_section = section.config
        facets = []
        for l in datatype.schema.settings["supported-langs"]:
            path = self.facet_path(datatype, facet_section)
            facet_definition = FacetDefinition(
                path=facet_name(datatype.path + "_" + l),
                dot_path=datatype.path + "." + l,
                searchable=facet_section.get("searchable"),
                imports=[
                    {
                        "import": "invenio_records_resources.services.records.facets.TermsFacet"
                    }
                ],
            )
            label = facet_section.get(
                "label", f'{datatype.path.replace(".", "/")}.label'
            )

            facet_definition.set_field(
                facet_section,
                arguments=[
                    f"field={repr(path + '.' + l+ '.keyword')}",
                    f"label =_({repr(label)})",
                    *facet_section.get("args", []),
                ],
                field_class="TermsFacet",
            )
            facets.extend(
                flatten(
                    datatypes.call_components(
                        datatype.parent,
                        "build_facet_definition",
                        facet_definition=facet_definition,
                    )
                )
            )
        section.config["facets"] = facets
        return section
