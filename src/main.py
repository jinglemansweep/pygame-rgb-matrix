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

# THEME STUFF

TILE_GRASS_EMPTY_ALT = 0
TILE_GRASS_EMPTY = 1
TILE_GRASS_BEACH = 2
TILE_GRASS_BEACH_ALT = 8
TILE_GRASS_ROCKS = 6
TILE_GRASS_WEEDS = 7

TILE_DESERT_EMPTY_ALT = 3
TILE_DESERT_EMPTY = 4
TILE_DESERT_BEACH = 5
TILE_DESERT_BEACH_ALT = 11
TILE_DESERT_ROCKS = 9
TILE_DESERT_WEEDS = 10

TILE_WAVES = 48
TILE_WAVES_ALT = 54

TILE_WATER_EMPTY = 49
TILE_WATER_LILY = 50
TILE_WATER_REEDS = 56

MAP_TILE_SIZE = 8
MAP_WIDTH = 32  # multiplied by tile size to get pixels
MAP_HEIGHT = 32  # multiplied by tile size to get pixels

SPRITE_TILES_FILE = f"{os.path.dirname(__file__)}/sprites/tiles.png"
SPRITE_ANIMALS_FILE = f"{os.path.dirname(__file__)}/sprites/animals.png"

tileset_bg = Tileset(SPRITE_TILES_FILE, (8, 8), 0, 0, 0.6)
tilemap_bg = Tilemap(tileset_bg, (8, 8))


def generate_row_land(width, alt_tiles=0, rock_tiles=0, weed_tiles=0, desert=False):
    start_tile = TILE_DESERT_EMPTY_ALT if desert else TILE_GRASS_EMPTY_ALT
    row = [start_tile + 1 for i in range(width)]
    for i in range(alt_tiles):
        row[random.randint(0, width - 1)] = start_tile
    for i in range(rock_tiles):
        row[random.randint(0, width - 1)] = start_tile + 6
    for i in range(weed_tiles):
        row[random.randint(0, width - 1)] = start_tile + 7
    print(row)
    return row


def generate_row_beach(width, alt_tiles=0, desert=False):
    start_tile = TILE_DESERT_EMPTY_ALT if desert else TILE_GRASS_EMPTY_ALT
    row = [start_tile + 2 for i in range(width)]
    for i in range(alt_tiles):
        row[random.randint(0, width - 1)] = start_tile + 8
    print(row)
    return row


def generate_row_waves(width, alt_tiles=0):
    row = [TILE_WAVES for i in range(width)]
    for i in range(alt_tiles):
        row[random.randint(0, width - 1)] = TILE_WAVES_ALT
    print(row)
    return row


def generate_row_water(width, lily_tiles=0, reed_tiles=0):
    row = [TILE_WATER_EMPTY for i in range(width)]
    for i in range(lily_tiles):
        row[random.randint(0, width - 1)] = TILE_WATER_LILY
    for i in range(reed_tiles):
        row[random.randint(0, width - 1)] = TILE_WATER_REEDS
    print(row)
    return row


row_beach = random.randint(3, 6)

game_map = []

for row in range(MAP_HEIGHT):
    if row < row_beach:
        game_map.append(
            generate_row_land(
                MAP_WIDTH,
                random.randint(0, 2),
                random.randint(0, 2),
                random.randint(0, 2),
            )
        )
    if row == row_beach:
        game_map.append(generate_row_beach(MAP_WIDTH, random.randint(0, 4)))
    if row == row_beach + 1:
        game_map.append(generate_row_waves(MAP_WIDTH, random.randint(0, 2)))
    if row > row_beach + 1:
        game_map.append(
            generate_row_water(MAP_WIDTH, random.randint(0, 8), random.randint(0, 8))
        )

tilemap_bg.set_map(game_map)
tilemap_bg.render()

tileset_animals = Tileset(SPRITE_ANIMALS_FILE, (8, 8), 0, 0, 0.9)

actors = pygame.sprite.Group()
x = 0
y = 0
for i in range(0, 16):
    sprite = BaseSprite(tileset_animals.tiles[i])
    sprite.rect.x = x
    sprite.rect.y = y
    actors.add(sprite)
    x += 8
    if x > LED_COLS:
        y += 8
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
    screen.blit(tilemap_bg.image, (0, 0))
    for idx, actor in enumerate(actors):
        actor.rect.x += 1
        if actor.rect.x > LED_COLS:
            actor.rect.y += 8
            actor.rect.x = -8
        if actor.rect.y >= 16:
            actor.rect.y = 0
        screen.blit(actor.image, actor.rect)
    render_pygame(screen, matrix)
    clock.tick(30)
    frame += 1


run()
