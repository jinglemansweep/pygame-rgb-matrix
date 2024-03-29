import logging
import pygame
from datetime import datetime
from pygame import SRCALPHA


logger = logging.getLogger("sprites.clock")

# ['bitstreamverasansmono', 'bitstreamverasans', 'anonymousprominus', 'anonymouspro', 'bitstreamveraserif']


class ClockWidgetSprite(pygame.sprite.DirtySprite):
    def __init__(
        self,
        rect,
        font_date="bitstreamverasans",
        font_time="bitstreamverasans",
        color_bg=(0, 0, 0),
        color_fg=(255, 255, 255),
        antialias=True,
        time_fmt="%H:%M",
    ):
        pygame.sprite.DirtySprite.__init__(self)
        self.rect = pygame.rect.Rect(*rect)
        self.image = pygame.Surface((self.rect.width, self.rect.height), SRCALPHA)
        pygame.font.init()
        self.font_date = pygame.font.SysFont(font_date, 20, bold=True)
        self.font_time = pygame.font.SysFont(font_time, 38, bold=True)
        self.color_bg = color_bg
        self.color_fg = color_fg
        self.antialias = antialias
        self.time_fmt = time_fmt
        self.sec_prev = None

    def update(self, frame: str, delta: float):
        super().update(frame)
        # Common updates
        now = datetime.now()
        # Only render text every new second
        if self.sec_prev is not None and now.second == self.sec_prev:
            return
        self.sec_prev = now.second
        dow_str = now.strftime("%A")[:3]
        ddmm_str = now.strftime("%d/%m")
        date_str = f"{dow_str} {ddmm_str}"
        time_str = now.strftime(self.time_fmt)
        shadow_depth = 2
        self.image.fill(self.color_bg)
        date_sprite = self.font_date.render(date_str, self.antialias, self.color_fg)
        date_sprite_shadow = self.font_date.render(date_str, self.antialias, (0, 0, 0))
        date_pos = ((self.rect[2] - date_sprite.get_rect()[2]) // 2, 40)
        time_sprite = self.font_time.render(time_str, self.antialias, self.color_fg)
        time_sprite_shadow = self.font_time.render(time_str, self.antialias, (0, 0, 0))
        time_pos = ((self.rect[2] - time_sprite.get_rect()[2]) // 2, -2)
        self.image.blit(
            date_sprite_shadow, (date_pos[0] + shadow_depth, date_pos[1] + shadow_depth)
        )
        self.image.blit(date_sprite, date_pos)
        self.image.blit(
            time_sprite_shadow,
            (time_pos[0] + shadow_depth, time_pos[1] + shadow_depth),
        )
        self.image.blit(time_sprite, time_pos)
        self.dirty = 1
