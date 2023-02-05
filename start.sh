#!/bin/bash

declare -r display="${1:-99}"

export DISPLAY=":${display}"

. ./venv/bin/activate

pushd ./src >/dev/null
python3 -m app
popd >/dev/null

