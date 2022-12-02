# pygame-rgb-matrix

PyGame RGB Matrix Framework for HUB75 LED Panels

## Installation

Create a `virtualenv` and install the project requirements:

    python3 -m venv ./venv
    source ./venv/bin/activate
    pip install -r ./requirements.txt

Clone and build [hzeller](https://github.com/hzeller)'s [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) Python bindings into the `lib` directory within the clone of this repository:

    mkdir ./lib
    cd ./lib
    git clone git@github.com:hzeller/rpi-rgb-led-matrix.git
    make build-python

## Deployment / Configuration

Modify any LED matrix settings and other configuration by modifying the provided [rgbmatrix.env](./etc/rgbmatrix.env) environment file, and then copy it to `/etc/default`:

    vim ./etc/rgbmatrix.env
    sudo cp ./etc/rgbmatrix.env /etc/default/rgbmatrix

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

It may be beneficial to develop locally using the local PyGame GUI and then deploy any changes to the Raspberry Pi when finished. This can be achieved using `rsync` over `ssh`. The following command will syncronise any changes (excluding cache and virtualenv resources) to the Raspberry Pi over the network. The following assumes the Raspberry Pi is accessible as `rpi.local` and the project is deployed to `/opt/pygame-rgb-matrix` already:

    rsync -avx \
      --exclude venv \
      --exclude __pycache__ \
      --exclude .git \
      . \
      rpi.local:/opt/pygame-rgb-matrix/

If using the provided systemd unit file, the project can be remotely restarted from the Raspberry Pi:

    ssh rpi.local
    ...
    sudo systemctl restart rgbservice
