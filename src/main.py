import asyncio
import os
import pygame
import pygame.pkgdata
import random
import sys
import traceback
import time
from pygame.locals import QUIT

sys.path.append(
    os.path.abspath(
        os.path.dirname(__file__) + "/../lib/rpi-rgb-led-matrix/bindings/python"
    )
)

from config import matrix_options, LED_ENABLED
from sprites import BaseSprite, BaseTilemap, BaseTileset, Camera
from utils import (
    render_pygame,
    build_pygame_screen,
    setup_mqtt_client,
)
from theme import Theme

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

frame = 0


theme = Theme(VIEWPORT_SIZE)


def run():
    print("start asyncio event loop")
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
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
    now = time.localtime()
    screen.fill((0, 0, 0))
    theme.update(frame)
    # blitting
    theme.blit(screen)
    # rendering
    render_pygame(screen, matrix)
    # frame end
    clock.tick()
    frame += 1


run()
