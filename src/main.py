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
from pygame.locals import QUIT

sys.path.append(
    os.path.abspath(
        os.path.dirname(__file__) + "/../lib/rpi-rgb-led-matrix/bindings/python"
    )
)

from config import (
    matrix_options,
    LED_ENABLED,
)
from utils.helpers import (
    render_pygame,
    build_pygame_screen,
    build_context,
    setup_logger,
    JoyPad,
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

pygame.init()
clock = pygame.time.Clock()

screen = build_pygame_screen()
joypad = JoyPad(0)

matrix = None
if LED_ENABLED:
    from rgbmatrix import RGBMatrix

    matrix = RGBMatrix(options=matrix_options)



theme = Theme()
frame = 0


def run():
    logger.info("start asyncio event loop")
    while True:
        try:
            main()
        except Exception as e:
            traceback.print_exc(file=sys.stdout)


def main():
    while True:
        tick()


def tick():
    global frame, screen
    # events
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            sys.exit()
    # frame start
    ctx = build_context(frame, screen)
    now = time.localtime()
    screen.fill((0, 0, 0))
    # updates
    theme.update(ctx)
    # blitting
    theme.blit(ctx)
    # rendering
    render_pygame(screen, matrix)
    # frame end
    clock.tick(100)
    frame += 1


if __name__ == "__main__":
    run()
