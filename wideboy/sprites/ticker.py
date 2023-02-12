import pygame
import logging

from pygame.locals import SRCALPHA

from wideboy.sprites.utils.images import load_resize_image

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
        scroll_speed=60.0,
        loop_count=0,
        autorun=True,
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
        self.loop_count = loop_count
        self.autorun = autorun
        self.image = None
        self.item_surfaces = list()
        self.font_cache = dict()
        self.loop_idx = 0
        self.dirty = 2
        self.render_surface()
        if self.autorun:
            self.run()

    def run(self, reset_position=True, reset_loop=True):
        if reset_position:
            self.reset_position()
        if reset_loop:
            self.loop_idx = 0
        self.next_loop(True)
        self.running = True

    def stop(self, now=False):
        self.repeat = False
        self.running = not now

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
        text_surface = self.font_cache.get(font).render(text, antialias, color)
        temp_surface = pygame.Surface(
            (text_surface.get_rect().width + 2, text_surface.get_rect().height + 2),
            SRCALPHA,
        )
        for offset in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            outline_surface = self.font_cache.get(font).render(
                text, antialias, (0, 0, 0, 255)
            )
            temp_surface.blit(outline_surface, (offset[0] + 1, offset[1] + 1))
        temp_surface.blit(text_surface, (1, 1))
        self.item_surfaces.append(temp_surface)

    def add_image_item(self, filename, size):
        self.item_surfaces.append(load_resize_image(filename, size))

    def reset_position(self):
        self.x = self.rect.width

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
        self.reset_position()

    def _get_surface_width(self, surface):
        return surface.get_rect().width + self.item_margin

    def next_loop(self, run_now=False):
        if run_now or self.x < 0 - self.image.get_rect().width:
            if self.loop_count == 0 or self.loop_idx < self.loop_count:
                self.loop_idx += 1
                logger.debug(
                    f"sprite:ticker:loop idx={self.loop_idx}/{self.loop_count}"
                )
                self.reset_position()

    def update(self, frame, delta):
        super().update()
        if self.running:
            self.x -= self.scroll_speed * delta
            self.next_loop()
        self.rect.x = int(self.x)
        # logger.debug(f"sprite:ticker x={self.rect.x}")
