#!/bin/bash

set -e

OAREPO_VERSION=${OAREPO_VERSION:-12}

BUILDER_VENV=".venv-builder"
if test -d $BUILDER_VENV ; then
	rm -rf $BUILDER_VENV
fi

python3 -m venv $BUILDER_VENV
. $BUILDER_VENV/bin/activate
pip install -U setuptools pip wheel oarepo-model-builder-ui

pip install -e ".[tests]"
pytest tests -vvv

# if exists OMB variable, install model builder in editable mode from this directory
if [ -n "$OMB" ]; then
  pip install -e $OMB --config-settings editable_mode=compat
fi

VENV_TESTS=".venv-tests"

if test -d example-model; then
	rm -rf example-model
fi
if test -d $VENV_TESTS ; then
	rm -rf $VENV_TESTS
fi
oarepo-compile-model ./tests/model.json5 --output-directory example-model -vvv

python3 -m venv $VENV_TESTS
source $VENV_TESTS/bin/activate

pip install -U setuptools pip wheel
pip install "oarepo[tests]==${OAREPO_VERSION}.*"
pip install "./example-model[tests]"
pytest ./example-model/tests -vvv
