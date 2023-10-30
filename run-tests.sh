#!/bin/bash

set -e

OAREPO_VERSION=${OAREPO_VERSION:-11}
OAREPO_VERSION_MAX=$((OAREPO_VERSION+1))

BUILDER_VENV=.venv
if test -d $BUILDER_VENV ; then
	rm -rf $BUILDER_VENV
fi

python3 -m venv $BUILDER_VENV
. $BUILDER_VENV/bin/activate
pip install -U setuptools pip wheel
pip install -e .


python3 -m venv .venv-tests
source .venv-tests/bin/activate

pip install -U setuptools pip wheel
pip install "oarepo>=$OAREPO_VERSION,<$OAREPO_VERSION_MAX"
pip install pyyaml opensearch-dsl
pip install -e tests/test_app
pip install pytest-invenio
pip install oarepo-model-builder

pytest tests -vvv