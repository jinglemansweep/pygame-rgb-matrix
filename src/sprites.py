import numpy as np
import pygame
import random
from pygame.locals import SRCALPHA

COLOR_SURFACE = (0, 0, 0)

_dummy_display = pygame.display.set_mode((1, 1))


class Camera:
    def __init__(
        self,
        map_size,
        viewport_size,
        tile_size,
        position=None,
        direction=None,
        speed=None,
    ):
        if position is None:
            position = [0, 0]
        if direction is None:
            direction = [0, 0]
        if speed is None:
            speed = [1, 1]
        self.map_size = map_size
        self.viewport_size = viewport_size
        self.tile_size = tile_size
        self.position = list(position)
        self.direction = list(direction)
        self.speed = list(speed)
        self.target_position = [None, None]

    def get_position(self):
        return (self.position[0], self.position[1])

    def set_target_position(self, position):
        for axis in [0, 1]:
            if position[axis] is not None:
                self.target_position[axis] = position[axis]

    def set_random_position(self, bounds=None):
        if bounds is None:
            bounds = [None, None]
        bound_x = (
            bounds[0]
            if bounds[0] is not None
            else (self.map_size[0] - self.viewport_size[0]) * self.tile_size[0]
        )
        bound_y = (
            bounds[1]
            if bounds[1] is not None
            else (self.map_size[1] - self.viewport_size[1]) * self.tile_size[1]
        )
        position = (
            random.randint(0, bound_x),
            random.randint(0, bound_y),
        )
        self.set_target_position(position)

    def update(self):
        self._set_motion_props()
        for axis in [0, 1]:
            self.position[axis] += self.direction[axis] * self.speed[axis]

    def _set_motion_props(self):
        for axis in [0, 1]:
            if self.target_position[axis] is not None:
                if self.target_position[axis] != self.position[axis]:
                    self.direction[axis] = (
                        1 if self.target_position[axis] > self.position[axis] else -1
                    )
                else:
                    self.direction[axis] = 0
                    self.target_position[axis] = None
                    self.position[axis] = float(round(self.position[axis]))


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, tileset, tile_index):
        super().__init__()
        self.tileset = tileset
        self.image = self.tileset.tiles[tile_index]
        self.rect = self.image.get_rect()

    def get_viewport_position(self, camera):
        return (self.rect[0] - camera.position[0], self.rect[1] - camera.position[1])


class BaseTileset:
    def __init__(self, file, size, margin=0, spacing=0, brightness=1.0):
        self.file = file
        self.size = size
        self.margin = margin
        self.spacing = spacing
        self._image = pygame.image.load(file).convert_alpha()
        if brightness < 1.0:
            value = int((1.0 - brightness) * 255)
            self._image.fill((value, value, value), special_flags=pygame.BLEND_RGB_SUB)
        self.image = self._image.copy()
        self.image.fill((255, 255, 255, 255), None, pygame.BLEND_RGBA_MULT)
        self.image.set_colorkey((0, 0, 0))
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

    def set_zero(self):
        self.map = np.zeros(self.size, dtype=int)
        self.render()

    def set_map(self, map):
        self.map = np.array(map)
        self.render()

    def __str__(self):
        return f"{self.__class__.__name__} {self.size}"
