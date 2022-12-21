import datetime
import logging
import os
import pygame
import random
from pygame.locals import *

from utils.camera import Projection
from utils.themes import BaseTheme

from .sprites import WallSprite

logger = logging.getLogger("theme")

THEME_DIR = os.path.dirname(__file__)
# FONT_PATH = f"{THEME_DIR}/fonts/boldmarker.otf"

pygame.font.init()
# FONT_LARGE = pygame.font.Font(FONT_PATH, 24)
# FONT_SMALL = pygame.font.Font(FONT_PATH, 14)

VIEWPORT_SIZE = (64, 64)
MAP_SIZE = (VIEWPORT_SIZE[0] * 4, VIEWPORT_SIZE[1])
CAMERA_BOUNDS = (MAP_SIZE[0] - VIEWPORT_SIZE[0], MAP_SIZE[1] - VIEWPORT_SIZE[1])

ROOF_FLOOR_WIDTH = 4


class Theme(BaseTheme):
    def __init__(self):
        self.projections = [
            Projection((0, 0, 64, 64)),
            Projection((64, 0, 64, 64), (72, 2)),
            Projection((128, 0, 64, 64), (128, 0)),
            Projection((192, 0, 64, 64), (183, 3)),
        ]
        self.roof_height = 8
        self.floor_height = 8
        self.roof_sprites = pygame.sprite.Group()
        self.floor_sprites = pygame.sprite.Group()
        for i in range(0, MAP_SIZE[0] // ROOF_FLOOR_WIDTH):
            self.roof_sprites.add(
                WallSprite(
                    x=(i + 1) * ROOF_FLOOR_WIDTH,
                    y=0,
                    width=ROOF_FLOOR_WIDTH,
                    height=self.roof_height,
                    map_width=MAP_SIZE[0],
                )
            )
            self.roof_height += random.randint(-1, 1)
            self.roof_height = max(min(self.roof_height, 10), 6)
            self.floor_sprites.add(
                WallSprite(
                    x=(i + 1) * ROOF_FLOOR_WIDTH,
                    y=VIEWPORT_SIZE[1] - self.floor_height - 10,
                    width=ROOF_FLOOR_WIDTH,
                    height=self.floor_height,
                    map_width=MAP_SIZE[0],
                )
            )
            self.floor_height += random.randint(-1, 1)
            self.floor_height = max(min(self.floor_height, 10), 6)

    def update(self, ctx):
        frame, screen, hass = ctx
        super().update(frame)
        self.roof_sprites.update(frame)
        self.floor_sprites.update(frame)
        for idx, p in enumerate(self.projections):
            p.update()

    def blit(self, ctx):
        frame, screen, hass = ctx
        super().blit(screen)
        for p in self.projections:
            for roof in self.roof_sprites:
                p.blit(roof.image, roof.rect, screen)
            for floor in self.floor_sprites:
                p.blit(floor.image, floor.rect, screen)
