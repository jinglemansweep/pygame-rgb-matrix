# PyGame IoT Framework for RGB LED Matrices

An attempt at an experimental but slightly opinionated IoT display framework utilising PyGame as a sprite and graphics engine running on a Raspberry Pi outputting to a standard HUB75 RGB LED matrix. PyGame is able to dump its display as an array of RGB values, which are perfect for driving an RGB Matrix using the [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) library by [hzeller](https://github.com/hzeller).

By utilising PyGame, we can leverage the awesome graphics, spriting and animation systems available as well as develop locally (without the need for a Raspberry Pi and RGB Matrix connected).

![Demo](./docs/images/demo.gif)

## Requirements

* Any Raspberry Pi with 40 pin headers
* RGB Matrix Hat (e.g. [AdaFruit RGB Matrix Bonnet](https://www.adafruit.com/product/3211) or [Electrodragon RGB LED Matrix Panel Drive Board](https://www.electrodragon.com/product/rgb-matrix-panel-drive-board-raspberry-pi/)) 
* HUB75(E) compatible LED matrix

## Components

* [PyGame](https://www.pygame.org/)
* [hzeller/rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix)
* [Tiny Ranch 8x8px Asset Pack](https://gvituri.itch.io/tiny-ranch)

## Installation

Clone repository (including dependency submodules):

    git clone --recurse https://github.com/jinglemansweep/pygame-rgb-matrix.git

Create a `virtualenv` and install the project requirements:

    python3 -m venv ./venv
    source ./venv/bin/activate
    pip install -r ./requirements.txt

Clone and pull both the [flaschen-taschen](https://github.com/hzeller/flaschen-taschen) library as well the [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) library dependency, both developed by [hzeller](https://github.com/hzeller). `flaschen-taschen` should be installed as a Git submodule in `lib/flaschen-taschen` and the `rpi-rgb-led-matrix` dependency should be installed as a recursive Git submodule in `lib/flaschen-taschen/server/rgb-matrix`.

Update and build `flaschen-taschen` dependencies:

    git submodule update --init --recursive

    cd ./lib/flaschen-taschen/server
    make FT_BACKEND=rgb-matrix # or "terminal"
    cd ./rgb-matrix
    make build-python
    