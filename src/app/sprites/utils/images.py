import glob
import logging
import os
import pygame
from PIL import Image

logging.getLogger("PIL").setLevel(logging.CRITICAL + 1)
logger = logging.getLogger("sprites.utils.images")


def load_and_resize_image(filename, size):
    with Image.open(filename) as im:
        im.thumbnail(size, Image.Resampling.LANCZOS)
        image = pygame.image.fromstring(im.tobytes(), im.size, im.mode).convert_alpha()
    return image


def glob_files(path=".", pattern="*.*"):
    return glob.glob(os.path.join(path, pattern))
