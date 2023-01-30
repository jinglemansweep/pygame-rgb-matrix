import pygame
import logging

logger = logging.getLogger("sprites")


class StageSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frame = 0

    def update(self, frame):
        self.frame = frame
