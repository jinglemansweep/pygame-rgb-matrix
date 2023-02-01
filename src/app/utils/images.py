import glob
import logging
import os
import pygame
import random
import sys
from pygame.locals import SRCALPHA
from PIL import Image

from app.config import PYGAME_BITS_PER_PIXEL

IMAGE_PATH = os.path.join("..", "images", "photos")

logging.getLogger("PIL").setLevel(logging.CRITICAL + 1)


logger = logging.getLogger("images")

image_cache = dict()


class ImageObject:
    def __init__(self, filename, transient=False):
        self.filename = filename
        self.transient = transient


class ImageSprite(pygame.sprite.DirtySprite):
    def __init__(
        self,
        rect,
        filename,
        scroll_speed,
        margin=0,
        padding=2,
        transient=False,
    ):
        pygame.sprite.DirtySprite.__init__(self)
        self.filename = filename
        self.margin = margin
        self.padding = padding
        self.scroll_speed = scroll_speed
        self.transient = transient
        rotation = random.randint(-5, 5)
        if image_cache.get(self.filename) is not None:
            image = image_cache.get(self.filename)
        else:
            # logger.debug(f"sprite:image:cache:miss filename={self.filename}")
            image = image_cache[self.filename] = self.load_image(self.filename)
            # self.image = pygame.transform.rotozoom(image, rotation, 1)
        self.image = pygame.Surface(
            (image.get_rect()[2] + self.padding, image.get_rect()[3]),
            0,
            depth=PYGAME_BITS_PER_PIXEL,
        )
        self.image.fill((0, 0, 0))
        self.image.blit(image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect[0], self.rect[1] = rect[0], rect[1]  # - abs(rotation)
        self.x_float = rect[0]
        self.dirty = 0

    def update(self, frame):
        self.x_float -= self.scroll_speed
        self.rect[0] = int(self.x_float)
        if self.rect[0] < 0 - self.get_width():
            # logger.debug(f"image:kill filename={self.filename}")
            self.kill()

    def load_image(self, filename):
        with Image.open(self.filename) as im:
            im.thumbnail((128, 64), Image.Resampling.LANCZOS)
            image = pygame.image.fromstring(
                im.tobytes(), im.size, im.mode
            ).convert_alpha()
        return image

    def get_width(self):
        return self.rect[2] + self.margin


class ImageWidget(pygame.sprite.DirtySprite):
    def __init__(
        self,
        rect,
        item_margin=0,
        item_padding=2,
        scroll_speed=0.5,
    ):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface(
            (rect[2], rect[3]), SRCALPHA, depth=PYGAME_BITS_PER_PIXEL
        )
        self.rect = list(rect)
        self.rect_start = list(self.rect[:])
        self.item_margin = item_margin
        self.item_padding = item_padding
        self.scroll_speed = scroll_speed
        self.sprites = pygame.sprite.Group()
        self.item_idx = 0
        self.items = []
        self.remaining = None
        self.dirty = 2
        self.get_images()

    def update(self, frame):
        super().update(frame)
        if self.remaining is None or self.remaining <= 0:
            image_sprite = self.build_next_sprite()
            if image_sprite:
                self.remaining = image_sprite.get_width()
                self.sprites.add(image_sprite)
        if self.remaining is not None and self.remaining > 0:
            self.remaining -= self.scroll_speed
        self.sprites.update(frame)
        self.sprites.draw(self.image)

    def expire_all(self):
        for item in self.items:
            item.transient = True

    def build_next_sprite(self):
        if not len(self.items):
            return
        # logger.debug(f"image: item_idx={self.item_idx} count={len(self.items)}")
        next_item = self.items[self.item_idx]
        if next_item.transient:
            self.items.pop(self.item_idx)
        else:
            self.item_idx += 1
        if self.item_idx + 1 > len(self.items):
            self.item_idx = 0
        return ImageSprite(
            (self.rect[2], 0),
            next_item.filename,
            self.scroll_speed,
            self.item_margin,
            self.item_padding,
            transient=next_item.transient,
        )

    def get_images(self):
        files = glob.glob(os.path.join(IMAGE_PATH, "*.*"))
        for file in files:
            self.items.append(ImageObject(file))
