#!/bin/bash

declare -r root_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../" &> /dev/null && pwd)"

source "${root_dir}/config.env"

export LED_ROWS LED_COLS LED_SLOWDOWN_GPIO 
export MQTT_HOST MQTT_PORT MQTT_USER MQTT_PASSWORD

env

"${root_dir}/venv/bin/python" "${root_dir}/src/main.py"
