import logging
import pygame
from datetime import datetime
from pygame.locals import SRCALPHA

from app.sprites.utils.images import load_resize_image, tile_image

logger = logging.getLogger("sprites.background")


class BackgroundSprite(pygame.sprite.DirtySprite):
    def __init__(self, filename, rect, size=None):
        pygame.sprite.DirtySprite.__init__(self)
        self.rect = pygame.rect.Rect(*rect)
        image = load_resize_image(filename, size)
        self.image = tile_image(image, (640, 64))

    def update(self, frame, delta):
        pass
