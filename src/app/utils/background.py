import logging
import os
import pygame

logger = logging.getLogger("background")


class Background(pygame.sprite.DirtySprite):
    def __init__(
        self,
        rect,
    ):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface((rect[2], rect[3]))
        self.rect = pygame.Rect(*rect)
        self.png = pygame.image.load(
            os.path.join("..", "images", "city.png")
        ).convert_alpha()
        tile_x = 0
        while tile_x < self.rect[2]:
            self.image.blit(self.png, (tile_x, 0))
            tile_x += self.png.get_rect()[2]

    def update(self, frame):
        super().update(frame)
