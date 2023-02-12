#!/bin/bash

declare -r base_dir="/opt/workspace"
declare -r module="wideboy"

cd ${base_dir}
${base_dir}/venv/bin/python -m ${module}
