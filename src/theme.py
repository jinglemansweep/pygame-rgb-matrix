import os
import pygame
import random
from pygame.locals import *
from sprites import BaseSprite, BaseTilemap, BaseTileset

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

TILE_ANIMAL_COW = 0
TILE_ANIMAL_XXX = 6
TILE_ANIMAL_PIG = 12
TILE_ANIMAL_SHEEP = 18
TILE_ANIMAL_GOOSE = 24
TILE_ANIMAL_DUCK = 30
TILE_ANIMAL_CHICKEN = 36
TILE_ANIMAL_CHICK = 42
TILE_ANIMAL_FOX = 48
TILE_ANIMAL_CAT_BLACK = 54
TILE_ANIMAL_DOG_ALSATION = 60
TILE_ANIMAL_DOG_HUSKY = 66
TILE_ANIMAL_DOG_COLLIE = 72
TILE_ANIMAL_CAT_BROWN = 80
TILE_ANIMAL_CAT_GINGER = 88
TILE_ANIMAL_CAT_BLACK = 94

MAP_WIDTH = 32  # multiplied by tile size to get pixels
MAP_HEIGHT = 32  # multiplied by tile size to get pixels
MAP_SIZE = (MAP_WIDTH, MAP_HEIGHT)
TILE_SIZE = (8, 8)

SPRITE_TILES_FILE = f"{os.path.dirname(__file__)}/sprites/tiles.png"
SPRITE_ANIMALS_FILE = f"{os.path.dirname(__file__)}/sprites/animals.png"

ANIMAL_CHOICES = [
    TILE_ANIMAL_COW,
    TILE_ANIMAL_PIG,
    TILE_ANIMAL_SHEEP,
    TILE_ANIMAL_GOOSE,
    TILE_ANIMAL_DUCK,
    TILE_ANIMAL_CHICKEN,
    TILE_ANIMAL_CHICK,
    TILE_ANIMAL_FOX,
]


class Theme:
    def __init__(self):
        self.map_size = MAP_SIZE
        self.tile_size = TILE_SIZE
        self.tileset_bg = BaseTileset(SPRITE_TILES_FILE, self.tile_size, 0, 0, 0.6)
        self.tileset_animals = BaseTileset(
            SPRITE_ANIMALS_FILE, self.tile_size, 0, 0, 0.9
        )
        self.row_beach = random.randint(3, self.map_size[1] // 2)
        self.tilemap_bg = BackgroundTilemap(
            self.tileset_bg, self.map_size, self.row_beach
        )
        self.actors_animals = pygame.sprite.Group()
        for i in range(0, 24):
            sprite = AnimalSprite(
                self.tileset_animals,
                random.choice(ANIMAL_CHOICES),
                (
                    random.randint(0, self.map_size[0] * self.tile_size[0]),
                    random.randint(0, (self.row_beach - 1) * self.tile_size[1]),
                ),
            )
            self.actors_animals.add(sprite)

    def blit(self, screen, camera):
        screen.blit(
            self.tilemap_bg.image,
            (0 - camera.get_position()[0], 0 - camera.get_position()[1]),
        )
        self.actors_animals.update()
        for idx, actor in enumerate(self.actors_animals):
            screen.blit(actor.image, actor.get_viewport_position(camera))


class AnimalSprite(BaseSprite):
    def __init__(self, tileset, tile_start_index=0, position=None):
        super().__init__(tileset, tile_start_index)
        if position is None:
            position = (0, 0)
        self.rect = position

    def update(self):
        print(self, "update")


class BackgroundTilemap(BaseTilemap):
    def __init__(self, tileset, size, row_beach):
        super().__init__(tileset, size)
        self.set_map(self.generate_random_map(row_beach))

    def generate_random_map(self, row_beach):
        map = []

        for row in range(MAP_HEIGHT):
            if row < row_beach:
                map.append(
                    self._generate_row_land(
                        MAP_WIDTH,
                        random.randint(0, 8),
                        random.randint(0, 8),
                        random.randint(0, 8),
                    )
                )
            if row == row_beach:
                map.append(self._generate_row_beach(MAP_WIDTH, random.randint(0, 4)))
            if row == row_beach + 1:
                map.append(self._generate_row_waves(MAP_WIDTH, random.randint(0, 2)))
            if row > row_beach + 1:
                alt_tiles = random.randint(0, 3) if row % 2 == 0 else 0
                map.append(self._generate_row_water(MAP_WIDTH, alt_tiles, alt_tiles))
        return map

    def _generate_row_land(
        self, width, alt_tiles=0, rock_tiles=0, weed_tiles=0, desert=False
    ):
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

    def _generate_row_beach(self, width, alt_tiles=0, desert=False):
        start_tile = TILE_DESERT_EMPTY_ALT if desert else TILE_GRASS_EMPTY_ALT
        row = [start_tile + 2 for i in range(width)]
        for i in range(alt_tiles):
            row[random.randint(0, width - 1)] = start_tile + 8
        print(row)
        return row

    def _generate_row_waves(self, width, alt_tiles=0):
        row = [TILE_WAVES for i in range(width)]
        for i in range(alt_tiles):
            row[random.randint(0, width - 1)] = TILE_WAVES_ALT
        print(row)
        return row

    def _generate_row_water(self, width, lily_tiles=0, reed_tiles=0):
        row = [TILE_WATER_EMPTY for i in range(width)]
        for i in range(lily_tiles):
            row[random.randint(0, width - 1)] = TILE_WATER_LILY
        for i in range(reed_tiles):
            row[random.randint(0, width - 1)] = TILE_WATER_REEDS
        print(row)
        return row
