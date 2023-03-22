#!/bin/bash

set -e

python3 -m venv .venv
.venv/bin/pip install -U setuptools pip wheel
.venv/bin/pip install -e .
.venv/bin/pip install oarepo-model-builder



BUILDER=.venv/bin/oarepo-compile-model


#if true ; then
#    test -d tests/test_app && rm -rf tests/test_app
#    ${BUILDER} tests/model.json5 --output-directory tests/test_app -vvv
#fi

python3 -m venv .venv-tests
source .venv-tests/bin/activate

pip install -U setuptools pip wheel
pip install pyyaml opensearch-dsl
pip install -e tests/test_app
pip install pytest-invenio
pip install oarepo-model-builder

pytest tests -vv