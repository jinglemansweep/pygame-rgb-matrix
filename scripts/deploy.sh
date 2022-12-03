#!/bin/bash

declare -r target_host="${1}"
declare -r target_path="/opt/pygame-rgb-matrix"

if [ -z "${target_host}" ]; then
  echo "Target host not specified!"
  exit 2
fi

rsync -avx ./requirements.* "${target_host}:${target_path}/"
rsync -avx --exclude-from=./.deploy.excludes ./src/ "${target_host}:${target_path}/src/"
