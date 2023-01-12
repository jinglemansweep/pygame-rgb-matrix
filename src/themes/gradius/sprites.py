import logging
import numpy as np
import pygame
import random
from pygame.locals import *
from utils.sprites import TilesetSprite, AnimationMixin, CollisionMixin
from utils.tiles.tilemap import BaseTilemap

logger = logging.getLogger("theme.sprites")


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width=16, height=8, color=(255, 255, 255)):
        super().__init__()
        self.image = pygame.Surface([width, height])
        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y

    def move(self, direction):
        logger.info(f"player move: to={direction}")
        self.rect[0] += direction[0]
        self.rect[1] += direction[1]


class WallSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, map_width, height=8, width=8, color=(128, 0, 0)):
        super().__init__()
        self.width = width
        self.height = height
        self.map_width = map_width
        self.image = pygame.Surface([width, height])
        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y
        self.speed = 8.0

    def update(self, frame, speed_adj=None):
        if speed_adj is not None:
            self.speed += speed_adj
        self.rect[0] -= self.speed
        if self.rect[0] < 1:
            self.rect[0] = self.map_width
