import pygame
from pygame.locals import SRCALPHA

_dummy_display = pygame.display.set_mode((1, 1))


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
