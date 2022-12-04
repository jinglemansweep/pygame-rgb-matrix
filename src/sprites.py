import numpy as np
import pygame
from pygame.locals import SRCALPHA

COLOR_SURFACE = (0, 0, 0)

_dummy_display = pygame.display.set_mode((1, 1))


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect()


class Tileset:
    def __init__(self, file, size=(8, 8), margin=0, spacing=0):
        self.file = file
        self.size = size
        self.margin = margin
        self.spacing = spacing
        self._image = pygame.image.load(file).convert_alpha()
        self.image = self._image.copy()
        self.image.fill((255, 255, 255, 255), None, pygame.BLEND_RGBA_MULT)
        # self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.tiles = []
        self.load()

    def load(self):
        self.tiles = []
        x0 = y0 = self.margin
        w, h = self.rect.size
        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing
        for x in range(x0, w, dx):
            for y in range(y0, h, dy):
                tile = pygame.Surface(self.size, SRCALPHA)
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)

    def __str__(self):
        return f"{self.__class__.__name__} file:{self.file} tile:{self.size}"


class Tilemap:
    def __init__(self, tileset, size=(4, 4), rect=None):
        self.size = size
        self.tileset = tileset
        self.map = np.zeros(size, dtype=int)
        h, w = self.size
        th, tw = self.tileset.size
        self.image = pygame.Surface((tw * w, th * h))
        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()

    def render(self):
        m, n = self.map.shape
        th, tw = self.tileset.size
        for i in range(m):
            for j in range(n):
                tile = self.tileset.tiles[self.map[i, j]]
                self.image.blit(tile, (j * tw, i * th))

    def set_zero(self):
        self.map = np.zeros(self.size, dtype=int)
        self.render()

    # Direction: Top to Bottom, Left to Right
    # 0 = Top Row, 41 = Bottom Row

    def set_map(self, map):
        self.map = np.array(map)

    def set_random(self):
        n = len(self.tileset.tiles)
        self.map = np.random.randint(n, size=self.size)
        self.render()

    def __str__(self):
        return f"{self.__class__.__name__} {self.size}"
