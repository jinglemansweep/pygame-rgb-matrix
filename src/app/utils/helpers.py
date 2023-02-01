import aiohttp
import asyncio
import async_timeout
import feedparser
import logging
import numpy as np
import pygame
import random
from PIL import Image

from app.config import (
    LED_ROWS,
    LED_COLS,
    LED_CHAIN,
    LED_PARALLEL,
    PYGAME_BITS_PER_PIXEL,
)

LOG_FORMAT = "%(message)s"


def setup_logger(debug=False):

    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO, format=LOG_FORMAT
    )


# PyGame renders wall like this:
#
# | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
#
# We need to render to the LED panels (if using
# parallel chains and panels are arranged on a single row):
#
# | 0 | 1 | 2 | 3 |
# | 4 | 5 | 6 | 7 |
#


def render_led_matrix(screen, matrix=None, matrix_surface=None):
    if not matrix:
        return
    # Blit first 4 panels to top row
    matrix_surface.blit(
        screen,
        (0, 0),
        (0, 0, LED_COLS * LED_CHAIN, LED_ROWS * 1),
    )
    # Blit next 4 panels to next row
    matrix_surface.blit(
        screen,
        (0, LED_ROWS),
        (LED_COLS * LED_CHAIN, 0, (LED_COLS * LED_CHAIN), LED_COLS),
    )
    # Convert PyGame surface to RGB byte array
    image_str = pygame.image.tostring(matrix_surface, "RGB", False)
    # Create a PIL compatible image from the byte array
    image_rgb = Image.frombytes(
        "RGB", (LED_COLS * LED_CHAIN, LED_ROWS * LED_PARALLEL), image_str
    )
    # Render PIL image to buffer
    matrix.SetImage(image_rgb)


def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


async def async_fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()


async def get_rss_items(loop, url):
    feed = None
    async with aiohttp.ClientSession(loop=loop) as session:
        html = await async_fetch(session, url)
        feed = feedparser.parse(html)
    return feed


def hass_to_color(rgb_dict, brightness=255):
    color = [
        rgb_dict.get("r") * (brightness / 255),
        rgb_dict.get("g") * (brightness / 255),
        rgb_dict.get("b") * (brightness / 255),
    ]
    return tuple(color)


def hass_to_visible(control, master):
    if not master:
        return 0
    return 1 if control else 0


class JoyPad:
    def __init__(self, device_index):
        pygame.joystick.init()
        self.joypad = pygame.joystick.Joystick(device_index)
        self.joypad.init()
        self.button = None
        self.direction = (0, 0)

    def process_event(self, event):
        if event.type == pygame.JOYBUTTONDOWN:
            self.button = event.dict["button"]
        if event.type == pygame.JOYHATMOTION:
            self.direction = event.dict["value"]
