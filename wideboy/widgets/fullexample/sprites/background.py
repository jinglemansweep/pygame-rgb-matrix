import logging
import pygame

from wideboy.utils.images import load_resize_image, tile_surface

logger = logging.getLogger("sprites.background")


class BackgroundSprite(pygame.sprite.DirtySprite):
    def __init__(
        self, filename: str, rect: pygame.Rect, size: tuple[int, int] = None
    ) -> None:
        pygame.sprite.DirtySprite.__init__(self)
        self.rect = pygame.rect.Rect(*rect)
        image = load_resize_image(filename, size)
        self.image = tile_surface(image, (640, 64))

    def update(self, frame: int, delta: float) -> None:
        pass
