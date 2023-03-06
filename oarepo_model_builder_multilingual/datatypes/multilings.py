from oarepo_model_builder.datatypes import DataType
from oarepo_model_builder.datatypes.containers import ObjectDataType, ArrayDataType
from oarepo_model_builder.utils.facet_helpers import facet_definiton, facet_name


class MultilingualDataType(ArrayDataType):
    schema_type = "property"
    mapping_type = "multilingual"
    marshmallow_field = "ma_fields.List"
    model_type = "multilingual"

    class ModelSchema(DataType.ModelSchema):
        pass

    #todo multilang facets
    def get_facet(self, stack, parent_path):
        key, field = facet_definiton(self)
        path = parent_path
        if len(parent_path) > 0 and self.key:
            path = parent_path + '.' + self.key + '.lang'
        elif self.key:
            path = self.key + '.lang'
        if field:
            return field, facet_name(path)
        else:
            return f"TermsFacet(field=\"{path}\")", facet_name(path)


class I18nDataType(ObjectDataType):
    schema_type = "property"
    mapping_type = "i18nStr"
    marshmallow_field = "ma_fields.Nested"
    model_type = "i18nStr"

    #todo multilang facets
    def get_facet(self, stack, parent_path):
        key, field = facet_definiton(self)
        path = parent_path
        if len(parent_path) > 0 and self.key:
            path = parent_path + '.' + self.key
        elif self.key:
            path = self.key
        if field:
            return field, facet_name(path)
        else:
            return f"TermsFacet(field=\"{path}\")", facet_name(path)
