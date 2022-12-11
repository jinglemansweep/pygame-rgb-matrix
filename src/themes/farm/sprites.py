import logging
import numpy as np
import pygame
import random
from utils.sprites import TilesetSprite, AnimationMixin, CollisionMixin
from utils.tiles.tilemap import BaseTilemap

logger = logging.getLogger("theme.sprites")

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

TILE_TO_SPECIES = {
    TILE_ANIMAL_COW: "cow",
    TILE_ANIMAL_XXX: "xxx",
    TILE_ANIMAL_PIG: "pig",
    TILE_ANIMAL_SHEEP: "sheep",
    TILE_ANIMAL_GOOSE: "goose",
    TILE_ANIMAL_DUCK: "duck",
    TILE_ANIMAL_CHICKEN: "chicken",
    TILE_ANIMAL_CHICK: "chick",
    TILE_ANIMAL_FOX: "fox",
    TILE_ANIMAL_CAT_BLACK: "cat (black)",
    TILE_ANIMAL_DOG_ALSATION: "dog (alsation)",
    TILE_ANIMAL_DOG_HUSKY: "dog (husky)",
    TILE_ANIMAL_DOG_COLLIE: "dog (collie)",
    TILE_ANIMAL_CAT_BROWN: "cat (brown)",
    TILE_ANIMAL_CAT_GINGER: "cat (ginger)",
}

NAMES = [
    "david",
    "robert",
    "lewis",
    "phil",
    "duncan",
    "susan",
    "geoff",
    "karen",
    "sharon",
    "tracey",
    "billy",
]


class AnimalSprite(AnimationMixin, CollisionMixin, TilesetSprite):
    ACTION_STILL = 0
    ACTION_WALKING = 1

    def __init__(
        self,
        sprite_frames,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.sprite_frames = sprite_frames
        self.sprite_frame_index = 0
        self.action = self.ACTION_STILL
        self.name = random.choice(NAMES)

    def update(self, frame):
        # sprite animation
        if self.action == self.ACTION_STILL:
            self.image = self.tileset.tiles[self.tile_index]
        elif self.action == self.ACTION_WALKING:
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
        collisions = self.get_collisions()
        if len(collisions):
            logger.info(f"{self.get_name()} collided")
            self.set_nearby_position(max_range=[16, 16])
        # move to a nearby location every once in a while
        if 0 < self._random_seed < 10:
            self.set_nearby_position(min_range=[4, 4], max_range=[16, 16])
        super().update(frame)
        logger.debug(f"sprite->update: timers={self.timers}")

    def set_nearby_position(self, max_range, min_range=[0, 0]):
        x = self.rect[0] + (
            random.choice([-1, 1]) * random.randrange(min_range[0], max_range[0])
        )
        y = self.rect[1] + (
            random.choice([-1, 1]) * random.randrange(min_range[1], max_range[1])
        )
        logger.info(
            f"{self.get_name()} moving nearby to={x},{y} (from={self.rect[0]},{self.rect[1]})"
        )
        self.set_target_position([x, y])

    def get_name(self):
        return f"{TILE_TO_SPECIES[self.tile_index]}: {self.name}"

    def __repr__(self):
        return self.get_name()


class BackgroundTilemap(BaseTilemap):
    def __init__(self, tileset, size, row_beach):
        super().__init__(tileset, size)
        self.row_beach = row_beach
        self.set_map(self.generate_random_map())

    def generate_random_map(self):
        map = []
        for row in range(self.size[1]):
            if row < self.row_beach:
                map.append(
                    self._generate_row_land(
                        self.size[0],
                        random.randint(0, 8),
                        random.randint(0, 8),
                        random.randint(0, 8),
                    )
                )
            if row == self.row_beach:
                map.append(self._generate_row_beach(self.size[0], random.randint(0, 4)))
            if row == self.row_beach + 1:
                map.append(
                    self._generate_row_waves(self.size[0], random.randint(4, 12))
                )
            if row > self.row_beach + 1:
                alt_tiles = random.randint(0, 3) if row % 2 == 0 else 0
                map.append(self._generate_row_water(self.size[0], alt_tiles, alt_tiles))
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
