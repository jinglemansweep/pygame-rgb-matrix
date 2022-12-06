import numpy as np
import os
import pygame
import random
from pygame.locals import *

from utils.camera import Camera
from utils.sprites import TilesetSprite, AnimationMixin, CollisionMixin
from utils.themes import BaseTheme
from utils.tiles.tilemap import BaseTilemap
from utils.tiles.tileset import BaseTileset

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
TILE_ANIMAL_CAT_GINGER = 86

TILE_STRUCTURE_HOUSE_RED = 0
TILE_STRUCTURE_HOUSE_GREY = 8
TILE_STRUCTURE_HOUSE_BROWN = 16
TILE_STRUCTURE_BARN_A = 17
TILE_STRUCTURE_HOUSE_BRICK = 24
TILE_STRUCTURE_BARN_B = 25

ACTION_STILL = 0
ACTION_WALKING = 1


ANIMAL_CHOICES = [
    TILE_ANIMAL_COW,
    TILE_ANIMAL_PIG,
    TILE_ANIMAL_SHEEP,
    TILE_ANIMAL_GOOSE,
    TILE_ANIMAL_DUCK,
    TILE_ANIMAL_CHICKEN,
    TILE_ANIMAL_CHICK,
    TILE_ANIMAL_FOX,
    TILE_ANIMAL_CAT_BLACK,
    TILE_ANIMAL_DOG_ALSATION,
    TILE_ANIMAL_DOG_HUSKY,
    TILE_ANIMAL_DOG_COLLIE,
    TILE_ANIMAL_CAT_BROWN,
    TILE_ANIMAL_CAT_GINGER,
]

STRUCTURE_BUILDING_CHOICES = [
    TILE_STRUCTURE_HOUSE_RED,
    TILE_STRUCTURE_HOUSE_GREY,
    TILE_STRUCTURE_HOUSE_BROWN,
    TILE_STRUCTURE_HOUSE_BRICK,
    TILE_STRUCTURE_BARN_A,
    TILE_STRUCTURE_BARN_B,
]

SPRITE_TILES_FILE = f"{os.path.dirname(__file__)}/sprites/tiles.png"
SPRITE_ANIMALS_FILE = f"{os.path.dirname(__file__)}/sprites/animals.png"
SPRITE_STRUCTURES_FILE = f"{os.path.dirname(__file__)}/sprites/structures.png"

MAP_SIZE = (32, 32)  # width, height (multiplied by TILE_SIZE to get pixels)
VIEWPORT_SIZE = (8, 8)  # side of viewport in tiles (not pixels)
MAP_TILE_SIZE = (8, 8)  # width, height
STRUCTURE_TILE_SIZE = (16, 16)


class Theme(BaseTheme):
    def __init__(self):
        self.camera = Camera(MAP_SIZE, VIEWPORT_SIZE, MAP_TILE_SIZE, speed=(0.5, 0.5))
        self.tileset_bg = BaseTileset(SPRITE_TILES_FILE, MAP_TILE_SIZE, 0, 0, 0.6)
        self.tileset_animals = BaseTileset(
            SPRITE_ANIMALS_FILE, MAP_TILE_SIZE, 0, 0, 0.9
        )
        self.tileset_structures = BaseTileset(
            SPRITE_STRUCTURES_FILE, STRUCTURE_TILE_SIZE, 0, 0, 0.9
        )
        self.row_beach = random.randint(MAP_SIZE[1] // 2, MAP_SIZE[1] - 4)
        self.tilemap_bg = BackgroundTilemap(self.tileset_bg, MAP_SIZE, self.row_beach)
        self.group_collidables = pygame.sprite.Group()

        for _ in range(0, 12):
            structure = TilesetSprite(
                tileset=self.tileset_structures,
                tile_index=random.choice(STRUCTURE_BUILDING_CHOICES),
                position=(
                    random.randint(0, MAP_SIZE[0] * MAP_TILE_SIZE[0]),
                    random.randint(0, (self.row_beach - 2) * MAP_TILE_SIZE[1]),
                ),
            )
            self.group_collidables.add(structure)
        self.actors_animals = pygame.sprite.Group()
        for _ in range(0, 100):
            animal = AnimalSprite(
                tileset=self.tileset_animals,
                tile_index=random.choice(ANIMAL_CHOICES),
                sprite_frames=3,
                position=(
                    random.randint(0, MAP_SIZE[0] * MAP_TILE_SIZE[0]),
                    random.randint(0, (self.row_beach - 1) * MAP_TILE_SIZE[1]),
                ),
                speed=[1, 1],
                bounds=[
                    MAP_SIZE[0] * MAP_TILE_SIZE[0],
                    self.row_beach * MAP_TILE_SIZE[1],
                ],
                collidables=self.group_collidables,
                move_every_x_frame=10,
                animate_every_x_frame=10,
            )
            self.actors_animals.add(animal)

    def update(self, frame):
        super().update(frame)
        self.tilemap_bg.update(frame)
        self.actors_animals.update(frame)
        if frame % 1000 == 0:
            self.camera.set_random_position((None, self.row_beach * MAP_TILE_SIZE[1]))

    def blit(self, screen):
        # print(f"theme->blit camera={self.camera.position}")
        super().blit(screen)
        screen.blit(
            self.tilemap_bg.image,
            (0 - self.camera.position[0], 0 - self.camera.position[1]),
        )

        for idx, structure in enumerate(self.group_collidables):
            screen.blit(structure.image, structure.get_viewport_position(self.camera))

        for idx, actor in enumerate(self.actors_animals):
            screen.blit(actor.image, actor.get_viewport_position(self.camera))


class AnimalSprite(AnimationMixin, CollisionMixin, TilesetSprite):
    def __init__(
        self,
        sprite_frames,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.sprite_frames = sprite_frames
        self.sprite_frame_index = 0
        self.action = ACTION_STILL

    def update(self, frame):
        # sprite animation
        if self.action == ACTION_STILL:
            self.image = self.tileset.tiles[self.tile_index]
        elif self.action == ACTION_WALKING:
            if frame % self.animate_every_x_frame == 0:
                self.image = self.tileset.tiles[
                    self.tile_index + 1 + self.sprite_frame_index
                ]
                self.image_orig = self.image.copy()
                self.sprite_frame_index += 1
                if self.sprite_frame_index > self.sprite_frames - 1:
                    self.sprite_frame_index = 0
        self.image = pygame.transform.flip(
            self.image_orig, self.direction_last[0] < 0, False
        )
        # if we collide with a building, move to somewhere else
        if self._collision_detect():
            self.stop()
            self.set_nearby_position()
        # move to a nearby location every once in a while
        if 0 < self._random_seed < 10:
            self.set_nearby_position()
        super().update(frame)
        # print(f"sprite->update: timers={self.timers}")

    def set_nearby_position(self, range=(MAP_TILE_SIZE[0] * 4, MAP_TILE_SIZE[1] * 4)):
        x = self.rect[0] + (
            random.choice([-1, 1])
            * random.randrange(MAP_TILE_SIZE[0], MAP_TILE_SIZE[0] * 2)
        )
        y = self.rect[1] + (
            random.choice([-1, 1])
            * random.randrange(MAP_TILE_SIZE[1], MAP_TILE_SIZE[1] * 2)
        )
        x_max = (MAP_TILE_SIZE[0] * MAP_SIZE[0]) - MAP_TILE_SIZE[0]
        y_max = (MAP_TILE_SIZE[1] * MAP_SIZE[1]) - MAP_TILE_SIZE[1]
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x > x_max:
            x = x_max
        if y > y_max:
            y = y_max
        # print(f"set_nearby_position: from=({self.rect[0]},{self.rect[1]}) to=({x},{y})")
        self.set_target_position((x, y))


class BackgroundTilemap(BaseTilemap):
    def __init__(self, tileset, size, row_beach):
        super().__init__(tileset, size)
        self.row_beach = row_beach
        self.set_map(self.generate_random_map())

    def generate_random_map(self):
        map = []
        for row in range(MAP_SIZE[1]):
            if row < self.row_beach:
                map.append(
                    self._generate_row_land(
                        MAP_SIZE[0],
                        random.randint(0, 8),
                        random.randint(0, 8),
                        random.randint(0, 8),
                    )
                )
            if row == self.row_beach:
                map.append(self._generate_row_beach(MAP_SIZE[0], random.randint(0, 4)))
            if row == self.row_beach + 1:
                map.append(self._generate_row_waves(MAP_SIZE[0], random.randint(4, 12)))
            if row > self.row_beach + 1:
                alt_tiles = random.randint(0, 3) if row % 2 == 0 else 0
                map.append(self._generate_row_water(MAP_SIZE[0], alt_tiles, alt_tiles))
        return map

    def update(self, frame):
        if frame % 50 == 0:
            self.map[self.row_beach + 1] = np.roll(self.map[self.row_beach + 1], 1)
            self.render()

    def _generate_row_land(
        self, width, alt_tiles=0, rock_tiles=0, weed_tiles=0, desert=False
    ):
        start_tile = TILE_DESERT_EMPTY_ALT if desert else TILE_GRASS_EMPTY_ALT
        row = [start_tile + 1 for i in range(width)]
        for _ in range(alt_tiles):
            row[random.randint(0, width - 1)] = start_tile
        for _ in range(rock_tiles):
            row[random.randint(0, width - 1)] = start_tile + 6
        for _ in range(weed_tiles):
            row[random.randint(0, width - 1)] = start_tile + 7
        return row

    def _generate_row_beach(self, width, alt_tiles=0, desert=False):
        start_tile = TILE_DESERT_EMPTY_ALT if desert else TILE_GRASS_EMPTY_ALT
        row = [start_tile + 2 for i in range(width)]
        for _ in range(alt_tiles):
            row[random.randint(0, width - 1)] = start_tile + 8
        return row

    def _generate_row_waves(self, width, alt_tiles=0):
        row = [TILE_WAVES for i in range(width)]
        for _ in range(alt_tiles):
            row[random.randint(0, width - 1)] = TILE_WAVES_ALT
        return row

    def _generate_row_water(self, width, lily_tiles=0, reed_tiles=0):
        row = [TILE_WATER_EMPTY for i in range(width)]
        for _ in range(lily_tiles):
            row[random.randint(0, width - 1)] = TILE_WATER_LILY
        for _ in range(reed_tiles):
            row[random.randint(0, width - 1)] = TILE_WATER_REEDS
        return row
