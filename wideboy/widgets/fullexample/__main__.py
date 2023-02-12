import asyncio
import cProfile
import logging
import os
import pygame
import pygame.pkgdata
import random
import sys
import traceback
from dotenv import load_dotenv, find_dotenv
from pygame import QUIT


load_dotenv(find_dotenv())

from wideboy.config import DEBUG, LED_ROWS, LED_COLS, IMAGE_PATH

from wideboy.utils.display import connect_flaschen_taschen
from wideboy.utils.images import glob_files
from wideboy.utils.helpers import setup_logger
from wideboy.utils.pygame import (
    setup_pygame,
    handle_event,
    main_entrypoint,
    run_loop,
    loop_debug,
    clock_tick,
)
from wideboy.widgets.fullexample.sprites.background import BackgroundSprite
from wideboy.widgets.fullexample.sprites.clock import ClockWidgetSprite
from wideboy.widgets.fullexample.sprites.ticker import TickerWidgetSprite
from wideboy.widgets.fullexample.utils import update_ticker, show_ticker

# Widget Metadata

_APP_NAME = "wideboy"
_APP_DESCRIPTION = "WideBoy RGB Matrix Platform"
_APP_VERSION = "0.0.1"

# Logging

setup_logger(debug=DEBUG)
logger = logging.getLogger(_APP_NAME)

# Configuration

CANVAS_WIDTH = int(os.environ.get("FULLEXAMPLE_CANVAS_WIDTH", LED_COLS * 12))
CANVAS_HEIGHT = int(os.environ.get("FULLEXAMPLE_CANVAS_HEIGHT", LED_ROWS * 1))
RSS_URL = os.environ.get(
    "FULLEXAMPLE_RSS_URL", "https://feeds.skynews.com/feeds/rss/home.xml"
)
TICKER_UPDATE_INTERVAL = int(os.environ.get("FULLEXAMPLE_TICKER_UPDATE_INTERVAL", 3600))
TICKER_DISPLAY_INTERVAL = int(
    os.environ.get("FULLEXAMPLE_TICKER_DISPLAY_INTERVAL", 900)
)

# PyGame & Display

ft = connect_flaschen_taschen((LED_COLS * 4, LED_ROWS * 3))
clock, screen = setup_pygame((CANVAS_WIDTH, CANVAS_HEIGHT), _APP_DESCRIPTION)

# Initialisation

logger.info(f"{_APP_DESCRIPTION} v{_APP_VERSION}")
logger.info(f"panel:size w={LED_COLS}px h={LED_ROWS}px")
logger.info(f"canvas:size: w={CANVAS_WIDTH}px h={CANVAS_HEIGHT}px")


running = True
frame = 0

# Main Loop


async def start_main_loop():

    global frame

    background_images = glob_files(os.path.join(IMAGE_PATH, "backgrounds"), "*.png")
    background = BackgroundSprite(
        random.choice(background_images),
        (0, 0, CANVAS_WIDTH, CANVAS_HEIGHT),
        (LED_COLS * 4, LED_ROWS * 4),
    )
    sprites = pygame.sprite.LayeredDirty(background=background)
    sprites.set_clip((0, 0, CANVAS_WIDTH, CANVAS_HEIGHT))

    sprite_ticker = TickerWidgetSprite(
        (0, 38, CANVAS_WIDTH, 26),
        item_margin=100,
        loop_count=3,
        autorun=True,
    )
    sprites.add(sprite_ticker)

    sprite_clock = ClockWidgetSprite(
        (CANVAS_WIDTH - 128, 0, 128, CANVAS_HEIGHT),
        color_bg=(128, 0, 0, 192),
    )
    sprites.add(sprite_clock)

    loop = asyncio.get_event_loop()
    asyncio.create_task(
        update_ticker(loop, sprite_ticker, RSS_URL, TICKER_UPDATE_INTERVAL, True)
    )
    asyncio.create_task(show_ticker(sprite_ticker, TICKER_DISPLAY_INTERVAL, True))

    while running:
        for event in pygame.event.get():
            handle_event(event)

        delta = clock_tick(clock)

        sprites.update(frame, delta)
        sprites.clear(screen, background.image)
        update_rects = sprites.draw(screen)

        pygame.display.update(update_rects)
        ft.send_surface(screen)

        loop_debug(frame, clock, delta)

        frame += 1
        await asyncio.sleep(0)


# Entrypoint

if __name__ == "__main__":
    main_entrypoint(run_loop(start_main_loop))
