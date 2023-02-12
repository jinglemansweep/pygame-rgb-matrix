import aiohttp
import asyncio
import async_timeout
import feedparser
import logging
import numpy as np
import pygame
import random
from PIL import Image

from wideboy.config import (
    LED_ROWS,
    LED_COLS,
    LED_CHAIN,
    LED_PARALLEL,
    FT_HOST,
    FT_PORT,
    FT_LAYER,
    FT_TRANSPARENT,
)

LOG_FORMAT = "%(message)s"


def setup_logger(debug=False):

    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO, format=LOG_FORMAT
    )


def parallelise_surface(surface):
    temp_surface = pygame.Surface(
        (LED_COLS * LED_CHAIN, LED_ROWS * LED_PARALLEL),
    )
    # Blit first 4 panels to top row
    temp_surface.blit(
        surface,
        (0, 0),  # (0, 0)
        (0, 0, LED_COLS * 4, LED_ROWS * 1),  # (0, 0, 256, 64)
    )
    # Blit next 4 panels to next row
    temp_surface.blit(
        surface,
        (0, LED_ROWS * 1),  # (0, 64)
        (LED_COLS * 4, 0, LED_COLS * 4, LED_ROWS * 1),  # (256, 0, 256, 64)
    )
    # Blit next 4 panels to next row
    temp_surface.blit(
        surface,
        (0, LED_ROWS * 2),  # (0, 128)
        (LED_COLS * 8, 0, LED_COLS * 4, LED_ROWS * 1),  # (512, 0, 256, 64)
    )
    return temp_surface


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
