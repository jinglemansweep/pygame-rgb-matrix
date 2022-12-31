import asyncio
import logging
import pygame
import random
from PIL import Image
from pygame.locals import QUIT, RESIZABLE, SCALED, BLEND_RGBA_ADD

from config import VIRTUAL_SCREEN_SIZE

EVDEV_KEY_ESCAPE = 1
EVDEV_KEY_CURSOR_UP = 103
EVDEV_KEY_CURSOR_DOWN = 108
EVDEV_KEY_CURSOR_LEFT = 105
EVDEV_KEY_CURSOR_RIGHT = 106
EVDEV_KEY_SPACE = 57


def setup_logger(debug=False):
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)


def build_pygame_screen():
    pygame.display.set_caption("RGB MATRIX")
    return pygame.display.set_mode(VIRTUAL_SCREEN_SIZE, SCALED | RESIZABLE, 32)


def render_pygame(screen, matrix=None):
    if matrix is not None:
        flipped = pygame.transform.flip(screen, True, False)
        screen.blit(
            flipped,
            (0, 0),
        )
        imgdata = pygame.surfarray.array3d(screen)
        image_rgb = Image.fromarray(imgdata, mode="RGB")
        matrix.SetImage(image_rgb)
    pygame.display.flip()


def build_context(frame, key, screen, hass):
    return (frame, key, screen, hass)
