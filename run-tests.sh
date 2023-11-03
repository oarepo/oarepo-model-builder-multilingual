#!/bin/bash

set -e

OAREPO_VERSION=${OAREPO_VERSION:-11}
OAREPO_VERSION_MAX=$((OAREPO_VERSION+1))

BUILDER_VENV=".venv-builder"
if test -d $BUILDER_VENV ; then
	rm -rf $BUILDER_VENV
fi

python3 -m venv $BUILDER_VENV
. $BUILDER_VENV/bin/activate
pip install "oarepo>=$OAREPO_VERSION,<$OAREPO_VERSION_MAX"
pip install -U setuptools pip wheel
pip install -e ".[tests]"
pytest tests -vvv

VENV_TESTS=".venv-tests"

if test -d tests/example-model; then
	rm -rf tests/example-model
fi
if test -d $VENV_TESTS ; then
	rm -rf $VENV_TESTS
fi
oarepo-compile-model ./tests/model.json5 --output-directory ./tests/example-model -vvv

python3 -m venv $VENV_TESTS
source $VENV_TESTS/bin/activate

pip install -U setuptools pip wheel
pip install "oarepo>=$OAREPO_VERSION,<$OAREPO_VERSION_MAX"
pip install "./tests/example-model[tests]"
pytest tests/example-model/tests
#pip install pyyaml opensearch-dsl
#pip install pytest-invenio
#pip install oarepo-model-builder