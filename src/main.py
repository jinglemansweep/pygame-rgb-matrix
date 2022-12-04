import asyncio

import os
import sys
import traceback
import time

sys.path.append(
    os.path.abspath(
        os.path.dirname(__file__) + "/../lib/rpi-rgb-led-matrix/bindings/python"
    )
)

import pygame
import pygame.pkgdata
import random
from pygame.locals import QUIT, RESIZABLE, SCALED

from config import matrix_options, LED_ENABLED, LED_ROWS, LED_COLS
from sprites import BaseSprite, BaseTilemap, BaseTileset
from utils import (
    render_pygame,
    build_pygame_screen,
    setup_mqtt_client,
    Camera,
)
from theme import Theme

COLOR = (255, 255, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_YELLOW_DARK = (31, 31, 31)
COLOR_MAGENTA = (255, 0, 255)
COLOR_MAGENTA_DARK = (63, 0, 63)
COLOR_GREY = (127, 127, 127)
COLOR_GREY_DARK = (15, 15, 15)
COLOR_WHITE = (255, 255, 255)
COLOR_BACKGROUND = (0, 0, 0)


VIEWPORT_WIDTH = 8  # number of tiles per row
VIEWPORT_HEIGHT = 8  # number of rows
VIEWPORT_SIZE = (VIEWPORT_WIDTH, VIEWPORT_HEIGHT)

matrix = None
if LED_ENABLED:
    from rgbmatrix import RGBMatrix

    matrix = RGBMatrix(options=matrix_options)


mqtt = setup_mqtt_client()

pygame.init()
screen = build_pygame_screen()
clock = pygame.time.Clock()

x = 0
y = 0
frame = 0

theme = Theme()

camera = Camera(
    theme.map_size,
    VIEWPORT_SIZE,
    theme.tile_size,
    (0, 0),
    (1, 1),
    (0.4, 0.1),
)


def run():
    print("start asyncio event loop")

    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            print(e)
        finally:
            print(f"asyncio restarting")
            time.sleep(1)
            asyncio.new_event_loop()


async def main():
    mqtt.loop_start()
    while True:
        await asyncio.create_task(tick())
        await asyncio.sleep(0.001)


async def tick():
    global camera, frame, screen
    # events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    # frame start
    screen.fill((0, 0, 0))
    camera.update()
    cx, cy = camera.get_position()
    now = time.localtime()
    # blitting
    theme.blit(screen, camera)
    # rendering
    render_pygame(screen, matrix)
    # frame end
    clock.tick(120)
    frame += 1


run()
