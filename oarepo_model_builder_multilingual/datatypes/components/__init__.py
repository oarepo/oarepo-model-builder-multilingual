from .facets.i18n import I18nStrFacetsComponent
from .mapping import (
    FieldMultilingualMappingComponent,
    RegularMultilingualMappingComponent,
)
from .marshmallow.i18n import I18nMarshmallowComponent
from .marshmallow.ui_i18n import UII18nMarshmallowComponent
from .model import MultilingualDumperModelComponent
from .multilingual.field import RegularMultilingualComponent

DEFAULT_COMPONENTS = [
    MultilingualDumperModelComponent,
    RegularMultilingualComponent,
    RegularMultilingualMappingComponent,
    FieldMultilingualMappingComponent,
    I18nStrFacetsComponent,
    I18nMarshmallowComponent,
    UII18nMarshmallowComponent,
]
