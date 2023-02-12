import logging
import pygame
from datetime import datetime
from pygame import SRCALPHA


logger = logging.getLogger("sprites.tray")


class TrayWidgetSprite(pygame.sprite.DirtySprite):
    def __init__(self, rect):
        pygame.sprite.DirtySprite.__init__(self)
        self.rect = pygame.rect.Rect(*rect)
        self.image = pygame.Surface((self.rect.width, self.rect.height), SRCALPHA)

    def update(self, frame: str, delta: float):
        super().update(frame)
