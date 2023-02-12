import glob
import logging
import os
import pygame
from PIL import Image

logging.getLogger("PIL").setLevel(logging.CRITICAL + 1)
logger = logging.getLogger("sprites.utils.images")


def load_image(filename):
    return Image.open(filename)


def load_resize_image(filename, size=None):
    im = load_image(filename)
    if size is not None:
        im.thumbnail(size, Image.Resampling.LANCZOS)
    image = pygame.image.fromstring(im.tobytes(), im.size, im.mode).convert_alpha()
    return image


def glob_files(path=".", pattern="*.*"):
    return glob.glob(os.path.join(path, pattern))


def tile_image(image, size):
    x = y = 0
    tiled_image = pygame.Surface(size)

    while y < size[1]:
        while x < size[0]:
            tiled_image.blit(image, (x, y))
            x += image.get_width()
        y += image.get_height()
        x = 0
    return tiled_image
