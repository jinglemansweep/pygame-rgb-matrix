import datetime
import logging
import os
import pygame
import random
from pygame.locals import *

from utils.camera import Camera, Projection
from utils.sprites import TilesetSprite
from utils.themes import BaseTheme
from utils.tiles.tileset import BaseTileset

from .sprites import AnimalSprite, BackgroundTilemap
from .sprites import (
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
)
from .sprites import (
    TILE_STRUCTURE_HOUSE_RED,
    TILE_STRUCTURE_HOUSE_GREY,
    TILE_STRUCTURE_HOUSE_BROWN,
    TILE_STRUCTURE_HOUSE_BRICK,
    TILE_STRUCTURE_BARN_A,
    TILE_STRUCTURE_BARN_B,
)

logger = logging.getLogger("theme")

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

THEME_DIR = os.path.dirname(__file__)

SPRITE_TILES_FILE = f"{THEME_DIR}/images/tiles.png"
SPRITE_ANIMALS_FILE = f"{THEME_DIR}/images/animals.png"
SPRITE_STRUCTURES_FILE = f"{THEME_DIR}/images/structures.png"
FONT_PATH = f"{THEME_DIR}/fonts/boldmarker.otf"


pygame.font.init()

FONT_LARGE = pygame.font.Font(FONT_PATH, 24)
FONT_SMALL = pygame.font.Font(FONT_PATH, 14)

MAP_SIZE = (32, 32)  # width, height (multiplied by TILE_SIZE to get pixels)
VIEWPORT_SIZE = (8, 8)  # side of viewport in tiles (not pixels)
MAP_TILE_SIZE = (8, 8)  # width, height
STRUCTURE_TILE_SIZE = (16, 16)

CAMERA_X_MAX = (MAP_SIZE[0] - VIEWPORT_SIZE[0]) * MAP_TILE_SIZE[0]
CAMERA_Y_MAX = (MAP_SIZE[1] - VIEWPORT_SIZE[1]) * MAP_TILE_SIZE[1]

DATE_POSITION = (0, (VIEWPORT_SIZE[1] * MAP_TILE_SIZE[1]) - 16)
TIME_POSITION = (0, -8)

TL = [0, 0]
TR = [CAMERA_X_MAX, 0]
BR = [CAMERA_X_MAX, CAMERA_Y_MAX]
BL = [0, CAMERA_Y_MAX]
C = [CAMERA_X_MAX // 2, CAMERA_Y_MAX // 2]

CAMERA_POSITIONS = [TL, TR, BR, BL, C]


class Theme(BaseTheme):
    def __init__(self):
        self.projections = [
            Projection((0, 0, 64, 64)),
            Projection((64, 0, 64, 64), (64, 0)),
            Projection((128, 0, 64, 64), (128, 0)),
            Projection((192, 0, 64, 64), (192, 0)),
        ]
        self.tileset_bg = BaseTileset(SPRITE_TILES_FILE, MAP_TILE_SIZE, 0, 0, 0.6)
        self.tileset_animals = BaseTileset(
            SPRITE_ANIMALS_FILE, MAP_TILE_SIZE, 0, 0, 0.9
        )
        self.tileset_structures = BaseTileset(
            SPRITE_STRUCTURES_FILE, STRUCTURE_TILE_SIZE, 0, 0, 0.9
        )
        self.row_beach = random.randint(MAP_SIZE[1] - 4, MAP_SIZE[1] - 2)
        self.tilemap_bg = BackgroundTilemap(self.tileset_bg, MAP_SIZE, self.row_beach)
        self.group_collidables = pygame.sprite.Group()
        for i in range(0, 12):
            position = (
                random.randint(0, MAP_SIZE[0] * MAP_TILE_SIZE[0]),
                random.randint(0, (self.row_beach - 2) * MAP_TILE_SIZE[1]),
            )
            # position = (random.randint(0, 64), random.randint(0, 64))
            structure = TilesetSprite(
                tileset=self.tileset_structures,
                tile_index=random.choice(STRUCTURE_BUILDING_CHOICES),
                position=position,
            )
            self.group_collidables.add(structure)
        self.actors_animals = pygame.sprite.Group()
        for _ in range(0, 100):
            self.actors_animals.add(self._build_random_animal())

    def update(self, ctx):
        frame, screen, hass = ctx
        super().update(frame)
        self.tilemap_bg.update(frame)
        self.actors_animals.update(frame)
        for idx, p in enumerate(self.projections):
            p.update()
            p.camera.position[0] += (idx + 1) * 0.01
            p.camera.position[1] += 0.01
            if p.camera.position[0] > CAMERA_X_MAX:
                p.camera.position[0] = 0
            if p.camera.position[1] > CAMERA_Y_MAX:
                p.camera.position[1] = 0

    def blit(self, ctx):
        frame, screen, hass = ctx
        visible = hass.store["power"].state["state"] == "ON"
        show_date = hass.store["show_date"].state["state"] == "ON"
        # logger.debug(f"theme->blit camera={self.camera.position}")
        super().blit(screen)
        if not visible:
            return
        for p in self.projections:
            p.blit(
                self.tilemap_bg.image,
                (0, 0),
                screen,
            )
            for structure in self.group_collidables:
                p.blit(structure.image, structure.rect, screen)
            for actor in self.actors_animals:
                p.blit(actor.image, actor.rect, screen)

        """
        screen.blit(
            self.tilemap_bg.image,
            (0 - self.camera.position[0], 0 - self.camera.position[1]),
            (0, 0, 64, 64),
        )


        for idx, structure in enumerate(self.group_collidables):
            screen.blit(
                structure.image,
                structure.get_viewport_position(self.camera),
                (0, 0, 64, 64),
            )

        for idx, actor in enumerate(self.actors_animals):
            screen.blit(
                actor.image, actor.get_viewport_position(self.camera), (0, 0, 64, 64)
            )

        screen.blit(
            self._render_clock(show_seconds=False),
            TIME_POSITION,
        )

        if show_date:
            screen.blit(
                self._render_date(),
                DATE_POSITION,
            )
        """

    def _build_random_animal(self):
        position = (
            random.randint(0, MAP_SIZE[0] * MAP_TILE_SIZE[0]),
            random.randint(0, (self.row_beach - 1) * MAP_TILE_SIZE[1]),
        )
        bounds = [
            0,
            0,
            MAP_SIZE[0] * MAP_TILE_SIZE[0],
            self.row_beach * MAP_TILE_SIZE[1],
        ]
        return AnimalSprite(
            tileset=self.tileset_animals,
            tile_index=random.choice(ANIMAL_CHOICES),
            sprite_frames=3,
            position=position,
            speed=[1, 1],
            bounds=bounds,
            collidables=self.group_collidables,
            move_every_x_frame=10,
            animate_every_x_frame=10,
        )

    def _render_clock(self, show_seconds=False):
        shadow_offset = 1
        shadow = FONT_LARGE.render(self._get_time_string(show_seconds), True, (0, 0, 0))
        clock = FONT_LARGE.render(
            self._get_time_string(show_seconds), True, (200, 200, 200)
        )
        x, y, w, h = clock.get_rect()
        img = pygame.Surface((w + shadow_offset, h + shadow_offset), SRCALPHA)
        img.blit(shadow, (shadow_offset, shadow_offset))
        img.blit(clock, (0, 0))
        return img

    def _render_date(self):
        shadow_offset = 1
        shadow = FONT_SMALL.render(self._get_date_string(), True, (0, 0, 0))
        date = FONT_SMALL.render(self._get_date_string(), True, (200, 200, 0))
        x, y, w, h = date.get_rect()
        img = pygame.Surface((w + shadow_offset, h + shadow_offset), SRCALPHA)
        img.blit(shadow, (shadow_offset, shadow_offset))
        img.blit(date, (0, 0))
        return img

    def _get_time_string(self, show_seconds):
        now = datetime.datetime.now()
        if show_seconds:
            fmt = "{:0>2d}:{:0>2d}:{:0>2d}"
            values = (now.hour, now.minute, now.second)
        else:
            fmt = "{:0>2d}:{:0>2d}"
            values = (now.hour, now.minute)
        return fmt.format(*values)

    def _get_date_string(self):
        now = datetime.datetime.now()
        fmt = "{:0>2d}/{:0>2d}"
        values = (now.day, now.month)
        return fmt.format(*values)
