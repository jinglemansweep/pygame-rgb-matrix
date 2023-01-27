import logging
import pygame
from datetime import datetime
from pygame.locals import RESIZABLE, SCALED, DOUBLEBUF, SRCALPHA

logger = logging.getLogger("ticker")


class ClockWidget(pygame.sprite.Sprite):
    def __init__(
        self,
        width,
        height,
        font="freesans",
        color_bg=(0, 0, 0),
        color_fg=(255, 255, 255),
        antialias=True,
        time_fmt="%H:%M",
    ):
        self.image = pygame.Surface((width, height), 16)
        self.rect = self.image.get_rect()
        pygame.font.init()
        self.font_date = pygame.font.SysFont(font, 20)
        self.font_time = pygame.font.SysFont(font, 36)
        self.color_bg = color_bg
        self.color_fg = color_fg
        self.antialias = antialias
        self.time_fmt = time_fmt

    def update(self, frame):
        now = datetime.now()
        date_str = now.strftime("%d/%m/%Y")
        date_pos = (6, 36)
        time_str = now.strftime(self.time_fmt)
        time_pos = (16, 0)
        shadow_depth = 2
        self.image.fill(self.color_bg)
        date_sprite = self.font_date.render(date_str, self.antialias, self.color_fg)
        date_sprite_shadow = self.font_date.render(date_str, self.antialias, (0, 0, 0))
        time_sprite = self.font_time.render(time_str, self.antialias, self.color_fg)
        time_sprite_shadow = self.font_time.render(time_str, self.antialias, (0, 0, 0))
        self.image.blit(
            date_sprite_shadow, (date_pos[0] + shadow_depth, date_pos[1] + shadow_depth)
        )
        self.image.blit(date_sprite, date_pos)
        self.image.blit(
            time_sprite_shadow,
            (time_pos[0] + shadow_depth, time_pos[1] + shadow_depth),
        )
        self.image.blit(time_sprite, time_pos)
