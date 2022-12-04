import asyncio

import os
import sys
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
from sprites import BaseSprite, Tilemap, Tileset
from utils import (
    build_random_color,
    render_pygame,
    build_pygame_screen,
    setup_mqtt_client,
)

COLOR = (255, 255, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_YELLOW_DARK = (31, 31, 31)
COLOR_MAGENTA = (255, 0, 255)
COLOR_MAGENTA_DARK = (63, 0, 63)
COLOR_GREY = (127, 127, 127)
COLOR_GREY_DARK = (15, 15, 15)
COLOR_WHITE = (255, 255, 255)
COLOR_BACKGROUND = (0, 0, 0)

SPRITE_TILES_FILE = f"{os.path.dirname(__file__)}/sprites/tiles.png"
SPRITE_ANIMALS_FILE = f"{os.path.dirname(__file__)}/sprites/animals.png"

tileset_bg = Tileset(SPRITE_TILES_FILE, (8, 8), 0, 0)
tilemap_bg = Tilemap(tileset_bg, (8, 8))


def generate_bg_row():
    row = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0, 2):
        row[random.randint(0, 7)] = 1
    if random.randint(0, 3) == 0:
        row[random.randint(0, 7)] = 6
    return row


tilemap_bg.set_map(
    [
        generate_bg_row(),
        generate_bg_row(),
        generate_bg_row(),
        generate_bg_row(),
        generate_bg_row(),
        generate_bg_row(),
        generate_bg_row(),
        generate_bg_row(),
    ]
)
tilemap_bg.render()

tileset_animals = Tileset(SPRITE_ANIMALS_FILE, (8, 8), 0, 0)

actors = pygame.sprite.Group()
x = 0
y = 0
for i in range(0, 16):
    sprite = BaseSprite(tileset_animals.tiles[i])
    sprite.rect.x = x
    sprite.rect.y = y
    actors.add(sprite)
    x += 16
    if x > LED_COLS:
        y += 16
        x = 0
    if y > LED_ROWS:
        y = 0
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


def run():
    print("start asyncio event loop")

    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            print("EXCEPTION", e)
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
    global frame, screen
    now = time.localtime()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((0, 0, 0))
    # screen.blit(tilemap_bg.image, (0, 0))
    for idx, actor in enumerate(actors):
        actor.rect.x += 1
        if actor.rect.x > LED_COLS:
            actor.rect.y += 16
            actor.rect.x = 0
        if actor.rect.y > LED_ROWS:
            actor.rect.y = 0
        screen.blit(actor.image, actor.rect)
    render_pygame(screen, matrix)
    clock.tick(120)
    frame += 1


run()
