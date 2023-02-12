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

from wideboy.config import (
    DEBUG,
    PYGAME_FPS,
    LED_CHAIN,
    LED_PARALLEL,
    LED_ROWS,
    LED_COLS,
    PANEL_ROWS,
    PANEL_COLS,
    RSS_URL,
    RSS_UPDATE_INTERVAL,
    IMAGE_PATH,
    TICKER_DISPLAY_INTERVAL,
)

from wideboy.utils.display import connect_flaschen_taschen
from wideboy.utils.images import glob_files
from wideboy.utils.helpers import setup_logger
from wideboy.utils.pygame import setup_pygame, handle_event, main_entrypoint, run_loop
from wideboy.widgets.fullexample.sprites.background import BackgroundSprite
from wideboy.widgets.fullexample.sprites.clock import ClockWidgetSprite
from wideboy.widgets.fullexample.sprites.ticker import TickerWidgetSprite
from wideboy.widgets.fullexample.utils import update_ticker, show_ticker

_APP_NAME = "wideboy"
_APP_DESCRIPTION = "WideBoy RGB Matrix Platform"
_APP_VERSION = "0.0.1"

setup_logger(debug=DEBUG)
logger = logging.getLogger(_APP_NAME)

ft = connect_flaschen_taschen()
clock, screen = setup_pygame(_APP_DESCRIPTION)

logger.info(f"{_APP_DESCRIPTION} v{_APP_VERSION}")
logger.info(f"panel:size w={LED_COLS}px h={LED_ROWS}px")
logger.info(f"wall:size: w={PANEL_COLS*LED_COLS}px h={PANEL_ROWS*LED_ROWS}px")
logger.info(f"wall:layout w={PANEL_COLS} h={PANEL_ROWS}")
logger.info(
    f"gui:size w={LED_COLS*LED_CHAIN}px h={LED_ROWS*LED_PARALLEL}px",
)


running = True
frame = 0


async def start_main_loop():

    global frame

    background_images = glob_files(os.path.join(IMAGE_PATH, "backgrounds"), "*.png")
    background = BackgroundSprite(
        random.choice(background_images),
        (0, 0, LED_COLS * PANEL_COLS, LED_ROWS * PANEL_ROWS),
        (LED_COLS * 4, LED_ROWS * 4),
    )
    sprites = pygame.sprite.LayeredDirty(background=background)
    sprites.set_clip((0, 0, LED_COLS * PANEL_COLS, LED_ROWS * PANEL_ROWS))

    sprite_ticker = TickerWidgetSprite(
        (0, 38, LED_COLS * PANEL_COLS, 26),
        item_margin=100,
        loop_count=3,
        autorun=True,
    )
    sprites.add(sprite_ticker)

    sprite_clock = ClockWidgetSprite(
        (LED_COLS * (PANEL_COLS - 2), 0, LED_COLS * 2, LED_ROWS * PANEL_ROWS),
        color_bg=(128, 0, 0, 192),
    )
    sprites.add(sprite_clock)

    loop = asyncio.get_event_loop()
    asyncio.create_task(
        update_ticker(loop, sprite_ticker, RSS_URL, RSS_UPDATE_INTERVAL, True)
    )
    asyncio.create_task(show_ticker(sprite_ticker, TICKER_DISPLAY_INTERVAL, True))

    while running:
        for event in pygame.event.get():
            handle_event(event)

        delta = clock.tick(PYGAME_FPS) / 1000

        sprites.update(frame, delta)
        sprites.clear(screen, background.image)
        update_rects = sprites.draw(screen)

        pygame.display.update(update_rects)
        ft.send_surface(screen)

        if frame % 200 == 0:
            logger.info(f"debug:clock fps={clock.get_fps()} delta={delta}")

        frame += 1
        await asyncio.sleep(0)


if __name__ == "__main__":
    main_entrypoint(run_loop(start_main_loop))
