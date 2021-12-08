# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# Invenio OpenID Connect is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


from __future__ import absolute_import, print_function

import pytest
import langcodes
import marshmallow
from marshmallow import ValidationError
from marshmallow.fields import Nested, List
import oarepo_model_builder_multilingual.schema as multilingual
# from oarepo_model_builder_multilingual.schema import MultilingualSchema


def test_withoutApp():
    print(langcodes.Language.get('ava').is_valid())
    class MD(marshmallow.Schema):
         title = List(Nested(multilingual.MultilingualSchema()))

    data = {'title':
       [{'lang': 'cs', 'value': 'xxx'}, {'lang': 'en', 'value': 'xxx'}, {'lang': '_', 'value': 'xxx'}]
    }

    assert data == MD().load(data)
    data = {'title':
        ['xx']
    }

    with pytest.raises(ValidationError):
        MD().load(data)

    data = {'title':
                [{'lang': 'cx', 'value': 'xxx'}, {'lang': 'en', 'value': 'xxx'}]
    }

    with pytest.raises(ValidationError):
        MD().load(data)


