import logging
import pygame

from wideboy.utils.images import load_resize_image, tile_surface

logger = logging.getLogger("sprites.background")


class BackgroundSprite(pygame.sprite.DirtySprite):
    def __init__(
        self,
        filename: str,
        rect: pygame.Rect,
        tile_size: tuple[int, int],
        fill_size: tuple[int, int],
    ) -> None:
        pygame.sprite.DirtySprite.__init__(self)
        self.rect = pygame.rect.Rect(*rect)
        image = load_resize_image(filename, tile_size)
        self.image = tile_surface(image, fill_size)
        self.dirty = 2

    def update(self, frame: int, delta: float) -> None:
        pass
