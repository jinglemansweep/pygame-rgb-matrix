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

Create a `virtualenv` and install the project requirements:

    python3 -m venv ./venv
    source ./venv/bin/activate
    pip install -r ./requirements.txt

The [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) library by [hzeller](https://github.com/hzeller)'s should be installed as a Git submodule in `lib/rpi-rgb-led-matrix`. Build the required Python bindings:

    git submodule update --init --recursive
    cd ./lib/rpi-rgb-led-matrix
    make build-python

## Configuration

Modify any LED matrix and other settings by copying and modifying the provided [config.env](./config.env.example) example file:

    cp ./config.env.example ./config.env
    vim ./config.env

## Starting / Testing

Use the provided helper [start.sh](./scripts/start.sh) script to start the application. It will automatically include your configuration in `config.env`:

    sudo ./scripts/start.sh

## Deployment / Configuration

Copy the provided [rgbmatrix.service](./etc/rgbmatrix.service) systemd unit definition file to `/etc/systemd/system`, reload the systemd daemon and then attempt to start the service:

    sudo cp ./etc/rgbmatrix.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl start rgbmatrix

If the LED matrix doesn't show any content, inspect the journal logs for information and modify any settings in `/etc/default/rgbmatrix`:

    sudo journalctl -n 200 -u rgbmatrix.service

If the service starts and you want to enable it to start automatically on every boot:

    sudo systemctl enable rgbmatrix

## Development (Locally)

The project can be started with a local PyGame GUI window for easier development and testing, providing the required desktop environment is installed and configured. The local GUI window can be enabled by setting the `GUI_ENABLED` environment variable to `true` (by default, the GUI is disabled).

It is also possible to start the project without initialising the underlying LED Matrix driver (for developing outside of the Raspberry Pi). The LED Matrix driver can be disabled by setting the `LED_ENABLED` environment variable to `false` (by default, the LED matrix is enabled).

To test locally with a PyGame GUI window and without initialising the RGB Matrix:

    source ./venv/bin/activate
    LED_ENABLED=false GUI_ENABLED=true python3 src/main.py

### Redeploying Changes

It may be beneficial to develop locally using the local PyGame GUI and then deploy any changes to the Raspberry Pi when finished. This can be achieved using `rsync` over `ssh`. The following command will syncronise any changes (excluding cache and virtualenv resources) to the Raspberry Pi over the network. The following assumes the Raspberry Pi is accessible as `rpi.local` and the project is deployed to `/home/user/pygame-rgb-matrix` already:

    rsync -avx \
      --exclude __pycache__ \
      ./src/ \
      rpi.local:/home/user/pygame-rgb-matrix/src/

If using the provided systemd unit file, the project can be remotely restarted from the Raspberry Pi:

    ssh rpi.local
    ...
    sudo systemctl restart rgbservice
