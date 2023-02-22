# this is the content of the templates/invenio_schema_multilingual.py.jinja2
# should find a better way of testing this, such as generating a sample app
# and running it

import langcodes
from marshmallow import Schema, ValidationError, fields, validates

"""
Marshmallow schema for multilingual strings. Consider moving this to a library, not generating
this for each project.
"""


class MultilingualSchema(Schema):
    lang = fields.String(required=True)
    value = fields.String(required=True)

    @validates("lang")
    def validate_lang(self, value):
        if value != "_" and not langcodes.Language.get(value).is_valid():
            raise ValidationError("Invalid language code")
