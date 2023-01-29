import logging
import os
import pygame
import sys
from pygame.locals import SRCALPHA

from config import PYGAME_BITS_PER_PIXEL
from utils.sprites import StageSprite

logger = logging.getLogger("ticker")


class Message:
    def __init__(self, text, transient):
        self.text = text
        self.transient = transient


class MessageSprite(pygame.sprite.Sprite):
    def __init__(
        self,
        position,
        text,
        font,
        color,
        margin,
        scroll_speed=1,
        antialias=True,
        transient=False,
    ):
        super().__init__()
        self.position = position
        self.text = text
        self.margin = margin
        self.scroll_speed = scroll_speed
        self.transient = transient
        self.image = font.render(self.text, antialias, color)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect[0], self.rect[1] = self.position[0], self.position[1]

    def update(self, frame):
        self.rect[0] -= self.scroll_speed
        if self.rect[0] < 0 - self.get_width():
            self.kill()

    def get_width(self):
        return self.rect[2] + self.margin


class TickerWidget(StageSprite):
    def __init__(
        self,
        rect,
        font="freesans",
        font_size=32,
        color_bg=(0, 0, 0, 0),
        color_fg=(255, 255, 255, 255),
        padding=0,
        item_margin=100,
        scroll_speed=1,
    ):
        super().__init__()
        self.image = pygame.Surface(
            (rect[2], rect[3]), SRCALPHA, depth=PYGAME_BITS_PER_PIXEL
        )
        self.rect = pygame.rect.Rect(*rect)
        self.rect_start = self.rect.copy()
        pygame.font.init()
        self.font = pygame.font.SysFont(font, font_size)
        self.color_bg = color_bg
        self.color_fg = color_fg
        self.padding = padding
        self.item_margin = item_margin
        self.scroll_speed = scroll_speed
        self.sprites = pygame.sprite.Group()
        self.items = []
        self.remaining = None

    def update(self, frame):
        super().update(frame)
        frame_rel = self.frame - self.mode_change_frame_start
        if self.remaining is None or self.remaining <= 0:
            current = self.get_next()
            self.remaining = current.get_width()
            self.sprites.add(current)
        if self.remaining > 0:
            self.remaining -= self.scroll_speed
        self.sprites.update(frame)
        self.image.fill(self.color_bg)
        self.sprites.draw(self.image)
        if self.mode == "idle":
            pass
        elif self.mode == "hiding":
            if self.rect[0] > self.rect_start[0] - self.rect_start[2]:
                self.rect[0] -= 4
            if frame_rel > self.rect_start[2] // 4:
                self.set_mode("idle")
        elif self.mode == "showing":
            if self.rect[0] < self.rect_start[0]:
                self.rect[0] += 4
            if frame_rel > self.rect_start[2] // 4:
                self.set_mode("idle")

    def add(self, text, transient=False):
        self.items.append(Message(text, transient))

    def get_next(self):
        if not len(self.items):
            return
        next_item = self.items.pop(0)
        if not next_item.transient:
            self.items.append(next_item)
        return MessageSprite(
            (self.rect[2], self.padding),
            text=next_item.text,
            font=self.font,
            color=self.color_fg,
            margin=self.item_margin,
            scroll_speed=self.scroll_speed,
            transient=next_item.transient,
        )
