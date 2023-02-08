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
from app.utils.flaschen import Flaschen

LOG_FORMAT = "%(message)s"

tf = Flaschen("rgbmatrix.home.ptre.es", 1337, 64, 64)


def setup_logger(debug=False):

    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO, format=LOG_FORMAT
    )


# PyGame renders wall like this:
#
# | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11
#
# We need to render to the LED panels (if using
# parallel chains and panels are arranged on a single row):
#
# |  0 |  1 |  2 |  3 | <- chain 1
# |  4 |  5 |  6 |  7 | <- chain 2
# |  8 |  9 | 10 | 11 | <- chain 3


def render_led_matrix(screen, matrix=None, matrix_surface=None, matrix_buffer=None):
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
    ).convert()

    # Render PIL image to buffer
    matrix_buffer.SetImage(image_rgb)
    # Flip and return next buffer
    return matrix.SwapOnVSync(matrix_buffer)


def render_tf(screen, matrix_surface=None):
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
    print(image_str)
    # Slice array to sections for offset overlay
    array_new = image_str[0:63, 0:63]
    tf.send_array(array_new, (0, 0, 1))
    print(len(array_new))


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
