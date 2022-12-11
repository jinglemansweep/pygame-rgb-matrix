#!/bin/bash

declare -r root_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../" &> /dev/null && pwd)"

set -a
source "${root_dir}/config.env"
set +a

"${root_dir}/venv/bin/python" "${root_dir}/src/main.py"
