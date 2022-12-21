import logging
import numpy as np
import pygame
import random
from pygame.locals import *
from utils.sprites import TilesetSprite, AnimationMixin, CollisionMixin
from utils.tiles.tilemap import BaseTilemap

logger = logging.getLogger("theme.sprites")


class WallSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, map_width, height=8, width=1, color=(128, 0, 0)):
        super().__init__()
        self.width = width
        self.height = height
        self.map_width = map_width
        self.image = pygame.Surface([width, height])
        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y

    def update(self, frame):

        self.rect[0] -= 1
        if self.rect[0] < 1:
            self.rect[0] = self.map_width
        # self.speed *= 1.0
