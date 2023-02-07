#!/bin/bash

LED_BRIGHTNESS=25
LED_ROWS=64
LED_COLS=64
LED_CHAIN=4
LED_PARALLEL=2
LED_SLOWDOWN_GPIO=3

FT_DIMENSIONS="256x128"


./lib/flaschen-taschen/server/ft-server \
  -D ${FT_DIMENSIONS} \
  --led-brightness=${LED_BRIGHTNESS} \
  --led-rows=${LED_ROWS} \
  --led-cols=${LED_COLS} \
  --led-chain=${LED_CHAIN} \
  --led-parallel=${LED_PARALLEL} \
  --led-slowdown-gpio=${LED_SLOWDOWN_GPIO}

