import numpy as np
import pygame


class BaseTilemap:
    def __init__(self, tileset, size=None, rect=None):
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

    def update(self):
        pass

    def set_zero(self):
        self.map = np.zeros(self.size, dtype=int)
        self.render()

    def set_map(self, map):
        self.map = np.array(map)
        self.render()

    def __str__(self):
        return f"{self.__class__.__name__} {self.size}"
