import numpy as np
import os
import pygame
from utils.camera import Camera


class BaseTheme:
    def __init__(self, viewport_size, map_size, tile_size):
        self.viewport_size = viewport_size
        self.map_size = map_size
        self.tile_size = tile_size
        self.camera = Camera(
            self.map_size, self.viewport_size, self.tile_size, speed=(0.5, 0.5)
        )

    def update(self, frame):
        self.camera.update()

    def blit(self, screen):
        pass
