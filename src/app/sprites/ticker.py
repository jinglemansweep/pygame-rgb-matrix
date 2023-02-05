import pygame
import logging

from pygame.locals import SRCALPHA

from app.sprites.utils.images import load_and_resize_image

logger = logging.getLogger("sprites.ticker")


class TickerWidgetSprite(pygame.sprite.DirtySprite):
    def __init__(
        self,
        rect,
        text_font="freesans",
        text_size=20,
        text_color=(255, 255, 255, 255),
        text_antialias=True,
        padding=0,
        item_margin=0,
        scroll_speed=1.0,
    ):
        super().__init__()
        pygame.font.init()
        self.rect = pygame.Rect(*rect)
        self.x, self.y = float(self.rect.x), float(self.rect.y)
        self.text_font = text_font
        self.text_size = text_size
        self.text_color = text_color
        self.text_antialias = text_antialias
        self.padding = padding
        self.item_margin = item_margin
        self.scroll_speed = scroll_speed
        self.image = None
        self.item_surfaces = list()
        self.font_cache = dict()
        self.dirty = 2
        self.render_surface()

    def clear_items(self):
        logger.debug(f"sprite:ticker:clear_items")
        self.items = list()
        self.item_surfaces = list()

    def add_text_item(self, text, font=None, size=None, color=None, antialias=None):
        font = font or self.text_font
        size = size or self.text_size
        color = color or self.text_color
        antialias = antialias or self.text_antialias
        if not self.font_cache.get(font):
            self.font_cache[font] = pygame.font.SysFont(font, size)
        self.item_surfaces.append(
            self.font_cache.get(font).render(text, antialias, color)
        )

    def add_image_item(self, filename, size):
        self.item_surfaces.append(load_and_resize_image(filename, size))

    def render_surface(self):
        surface_width = 0
        for item_surface in self.item_surfaces:
            surface_width += self._get_surface_width(item_surface)
        sprite_surface = pygame.Surface(
            (surface_width, self.rect.height), SRCALPHA, depth=16
        )
        blit_x = 0
        for item_surface in self.item_surfaces:
            sprite_surface.blit(item_surface, (blit_x, 0))
            blit_x += self._get_surface_width(item_surface)
        logger.debug(
            f"sprite:ticker:render_surface width={sprite_surface.get_rect().width} height={sprite_surface.get_rect().height}"
        )
        self.image = sprite_surface

    def _get_surface_width(self, surface):
        return surface.get_rect().width + self.item_margin

    def update(self, frame):
        super().update(frame)
        self.x -= self.scroll_speed
        if self.x < 0 - self.image.get_rect().width:
            self.x = self.rect.width
        self.rect.x = int(self.x)
        # logger.debug(f"sprite:ticker x={self.rect.x}")
