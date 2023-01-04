import asyncio
import curses
import logging
import os
import pygame
import pygame.pkgdata
import socket
import sys
import traceback
import time
import uuid
from argparse import ArgumentParser
from evdev import InputDevice, list_devices, ecodes
from pygame.locals import QUIT

sys.path.append(
    os.path.abspath(
        os.path.dirname(__file__) + "/../lib/rpi-rgb-led-matrix/bindings/python"
    )
)

from config import (
    matrix_options,
    LED_ENABLED,
    EVDEV_NAME,
    EVDEV_REPEAT_DELAY,
    EVDEV_REPEAT_RATE,
)
from integrations import setup_mqtt_client, HASSManager
from utils.helpers import (
    render_pygame,
    build_pygame_screen,
    build_context,
    setup_logger,
    get_evdev_key,
)
from themes.gradius import Theme

_APP_NAME = "matrixclock"
_APP_DESCRIPTION = "RGB Matrix Clock"
_APP_VERSION = "0.0.1"

parser = ArgumentParser(description=f"{_APP_DESCRIPTION} v{_APP_VERSION}")
parser.add_argument("-v", "--verbose", action="store_true")

args = parser.parse_args()
setup_logger(debug=args.verbose)
logger = logging.getLogger("main")

device_id = uuid.getnode()

devices = [InputDevice(fn) for fn in list_devices()]
device_found = False
dev = None
for dev in devices:
    print(dev.name)
    if dev.name == EVDEV_NAME:
        device_found = True
        dev.repeat = (EVDEV_REPEAT_RATE, EVDEV_REPEAT_DELAY)
        break
if not device_found:
    print(f"Input device '{EVDEV_NAME}' not found")

matrix = None
if LED_ENABLED:
    from rgbmatrix import RGBMatrix

    matrix = RGBMatrix(options=matrix_options)

store = dict()

mqtt = setup_mqtt_client()


hass = HASSManager(mqtt, device_id, _APP_NAME)
hass.add_entity("power", "Power", "switch", {}, dict(state="ON"))
hass.add_entity("show_date", "Show Date", "switch", {}, dict(state="ON"))


def _on_message(client, userdata, msg):
    hass.process_message(str(msg.topic), str(msg.payload))


mqtt.on_message = _on_message


pygame.init()
screen = build_pygame_screen()
clock = pygame.time.Clock()

theme = Theme()
frame = 0


def run():
    logger.info("start asyncio event loop")
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
        finally:
            logger.warning(f"asyncio restarting")
            time.sleep(1)
            asyncio.new_event_loop()


async def main():
    mqtt.loop_start()
    while True:
        await asyncio.create_task(tick())


async def tick():
    global frame, screen
    # events
    key = get_evdev_key(dev)
    if key is not None:
        print(key)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    # frame start
    ctx = build_context(frame, key, screen, hass)
    now = time.localtime()
    screen.fill((0, 0, 0))
    # updates
    theme.update(ctx)
    # blitting
    theme.blit(ctx)
    # rendering
    render_pygame(screen, matrix)
    # frame end
    # logger.debug(store)
    clock.tick(320)
    frame += 1


if __name__ == "__main__":
    run()
