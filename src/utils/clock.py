import logging
import pygame
from datetime import datetime
from enum import Enum
from pygame.locals import RESIZABLE, SCALED, DOUBLEBUF, SRCALPHA
from utils.sprites import StageSprite

logger = logging.getLogger("ticker")


class ClockWidget(StageSprite):
    def __init__(
        self,
        rect,
        font_date="arial",
        font_time="impact",
        color_bg=(0, 0, 0),
        color_fg=(255, 255, 255),
        antialias=True,
        time_fmt="%H:%M",
    ):
        super().__init__()
        self.image = pygame.Surface((rect[2], rect[3]), 16)
        self.rect = pygame.rect.Rect(*rect)
        self.rect_start = self.rect.copy()
        pygame.font.init()
        self.font_date = pygame.font.SysFont(font_date, 20)
        self.font_time = pygame.font.SysFont(font_time, 42)
        self.color_bg = color_bg
        self.color_fg = color_fg
        self.antialias = antialias
        self.time_fmt = time_fmt

    def update(self, frame):
        super().update(frame)
        # Common updates
        now = datetime.now()
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
        time_pos = ((self.rect[2] - time_sprite.get_rect()[2]) // 2, -6)
        self.image.blit(
            date_sprite_shadow, (date_pos[0] + shadow_depth, date_pos[1] + shadow_depth)
        )
        self.image.blit(date_sprite, date_pos)
        self.image.blit(
            time_sprite_shadow,
            (time_pos[0] + shadow_depth, time_pos[1] + shadow_depth),
        )
        self.image.blit(time_sprite, time_pos)
        # Mode handling
        frame_rel = self.frame - self.mode_change_frame_start
        if self.mode == "idle":
            pass
        elif self.mode == "hiding":
            if self.rect[0] < self.rect_start[0] + self.rect_start[2]:
                self.rect[0] += 1
            if frame_rel > self.rect_start[2]:
                self.set_mode("idle")
        elif self.mode == "showing":
            if self.rect[0] > self.rect_start[0]:
                self.rect[0] -= 1
            if frame_rel > self.rect_start[2]:
                self.set_mode("idle")
