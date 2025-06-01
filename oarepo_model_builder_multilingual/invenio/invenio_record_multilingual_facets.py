from oarepo_model_builder.invenio.invenio_record_facets import InvenioRecordSearchFacetsBuilder, get_distinct_facets
import re
from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder

class InvenioRecordMultilingualSearchFacetsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_search_options"
    section = "search-options"
    template = "record-search-options"

    def finish(self, **extra_kwargs):

        facets = get_distinct_facets(self.current_model)
        package = self.current_model.definition["facets"]["module"]

        imports = []
        for f in facets:
            imports.extend(f.imports)

        for facet in facets:
            field = facet.field

            if "MultilingualFacet" in field:

                match = re.search(r"MultilingualFacet\(lang_facets\s*=\s*\{(.*?)\},\s*label=_[^\)]+", field)
                if match:
                    dict_content = match.group(1)

                    dict_content = re.sub(r": '([^']+)'", r": \1", dict_content)

                    label_match = re.search(r"label=([^\)]+)", field)
                    if label_match:
                        label_content = label_match.group(0)
                        facet.field = f"MultilingualFacet(lang_facets={{ {dict_content} }}, {label_content}))"


        return super().finish(
            current_package_name=package,
            facets=facets,
            facet_imports=imports,
            **extra_kwargs,
        )
