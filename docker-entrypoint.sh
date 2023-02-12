#!/bin/bash

declare -r base_dir="/opt/workspace"

cd ${base_dir}/src
${base_dir}/venv/bin/python -m app
