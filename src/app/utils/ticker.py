import logging
import os
import pygame
import sys
from pygame.locals import SRCALPHA

from app.config import PYGAME_BITS_PER_PIXEL

logger = logging.getLogger("ticker")


class Message:
    def __init__(self, text, transient=False):
        self.text = text
        self.transient = transient


class MessageSprite(pygame.sprite.DirtySprite):
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
        pygame.sprite.DirtySprite.__init__(self)
        self.position = position
        self.text = text
        self.margin = margin
        self.scroll_speed = scroll_speed
        self.transient = transient
        self.image = font.render(self.text, antialias, color)
        self.rect = self.image.get_rect()
        self.reset()
        self.dirty = 2

    def reset(self):
        self.rect[0], self.rect[1] = self.position[0], self.position[1]

    def update(self, frame):
        self.rect[0] -= self.scroll_speed
        if self.rect[0] < 0 - self.get_width():
            self.kill()

    def get_width(self):
        return self.rect[2] + self.margin


class TickerWidget(pygame.sprite.DirtySprite):
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
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface((rect[2], rect[3]), SRCALPHA, depth=16)
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
        self.item_idx = 0
        self.items = []
        self.remaining = None
        self.dirty = 2

    def update(self, frame):
        super().update(frame)
        if self.remaining is None or self.remaining <= 0:
            message_sprite = self.build_next_sprite()
            if message_sprite:
                self.remaining = message_sprite.get_width()
                self.sprites.add(message_sprite)
        if self.remaining is not None and self.remaining > 0:
            self.remaining -= self.scroll_speed
        self.sprites.update(frame)
        self.image.fill(self.color_bg)
        self.sprites.draw(self.image)

    def add(self, text, transient=False):
        self.items.append(Message(text, transient))

    def expire_all(self):
        for item in self.items:
            item.transient = True

    def build_next_sprite(self):
        if not len(self.items):
            return
        # logger.debug(f"ticket: item_idx={self.item_idx} count={len(self.items)}")
        next_item = self.items[self.item_idx]
        if next_item.transient:
            self.items.pop(self.item_idx)
        else:
            self.item_idx += 1
        if self.item_idx + 1 > len(self.items):
            self.item_idx = 0
        return MessageSprite(
            (self.rect[2], self.padding),
            text=next_item.text,
            font=self.font,
            color=self.color_fg,
            margin=self.item_margin,
            scroll_speed=self.scroll_speed,
            transient=next_item.transient,
        )
