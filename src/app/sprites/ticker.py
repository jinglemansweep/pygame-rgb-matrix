import pygame

from pygame.locals import SRCALPHA
from app.sprites.base import BaseGroup


class TickerWidget(BaseGroup):
    def __init__(
        self,
        rect,
        items=None,
        font="freesans",
        font_size=32,
        color_bg=(0, 0, 0, 0),
        color_fg=(255, 255, 255, 255),
        antialias=True,
        padding=0,
        item_margin=100,
        scroll_speed=1,
    ):
        BaseGroup.__init__(self)
        pygame.font.init()
        self.font = pygame.font.SysFont(font, font_size)
        self.rect = rect
        if items is None:
            items = []
        self.items = items
        self.color_bg = color_bg
        self.color_fg = color_fg
        self.antialias = antialias
        self.padding = padding
        self.item_margin = item_margin
        self.scroll_speed = scroll_speed
        self.image = None
        self.dirty = 2
        self.render_sprite_surface()

    def render_sprite_surface(self):
        surface_width = 0
        text_surfaces = []
        for item in self.items:
            text_surface = self.font.render(self.text, self.antialias, self.color_fg)
            text_surfaces.append(text_surface)
            surface_width += self._get_text_surface_width(text_surface)
        sprite_surface = pygame.Surface(
            (surface_width, self.rect.height), SRCALPHA, depth=16
        )
        blit_x = 0
        for text_surface, idx in enumerate(text_surfaces):
            text_surface.blit(sprite_surface, (blit_x, 0))
            blit_x += self._get_text_surface_width(text_surface)
        self.sprite = pygame.sprite.DirtySprite()
        self.sprite.image = sprite_surface
        self.sprite.rect = sprite_surface.get_rect()
        self.add(self.sprite)

    def _get_text_surface_width(self, text_surface):
        return text_surface.get_rect().width + self.item_margin

    def update(self, frame):
        super().update(frame)
