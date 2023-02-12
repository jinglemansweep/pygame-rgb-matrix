import asyncio
import logging
import os
import pygame
import pygame.pkgdata
import random
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

from wideboy import _APP_NAME
from wideboy.config import DEBUG, IMAGE_PATH, FT_SIZE
from wideboy.utils.display import connect_flaschen_taschen
from wideboy.utils.helpers import (
    intro_debug,
    get_widget_name_from_path,
    get_config_env_var,
)
from wideboy.utils.images import glob_files
from wideboy.utils.logger import setup_logger
from wideboy.utils.pygame import (
    setup_pygame,
    handle_event,
    main_entrypoint,
    run_loop,
    loop_debug,
    clock_tick,
)
from wideboy.widgets.tray.sprites.tray import TrayWidgetSprite

# Widget Metadata

_WIDGET_NAME = get_widget_name_from_path(__file__)

# Logging

setup_logger(debug=DEBUG)
logger = logging.getLogger(_APP_NAME)

# Startup

intro_debug(_WIDGET_NAME)

# Configuration

CANVAS_WIDTH = int(get_config_env_var("CANVAS_WIDTH", 64 * 2, _WIDGET_NAME))
CANVAS_HEIGHT = int(get_config_env_var("CANVAS_HEIGHT", 26 * 1, _WIDGET_NAME))
CANVAS_SIZE = (CANVAS_WIDTH, CANVAS_HEIGHT)

logger.info(f"Canvas Size: {CANVAS_SIZE[0]}x{CANVAS_SIZE[1]}")

# PyGame & Display

ft = connect_flaschen_taschen()
clock, screen = setup_pygame(CANVAS_SIZE)

# Loop Setup

running = True

# Main Loop


async def start_main_loop():

    loop = asyncio.get_event_loop()

    background = pygame.surface.Surface(CANVAS_SIZE)
    background.fill((64, 0, 64, 255))
    sprites = pygame.sprite.LayeredDirty(background=background)
    sprites.set_clip((0, 0, *CANVAS_SIZE))

    sprite_tray = TrayWidgetSprite(
        (0, 0, *CANVAS_SIZE),
    )
    sprites.add(sprite_tray)

    while running:
        for event in pygame.event.get():
            handle_event(event)

        frame, delta = clock_tick(clock)

        sprites.update(frame, delta)
        sprites.clear(screen, background)
        update_rects = sprites.draw(screen)

        pygame.display.update(update_rects)
        ft.send_surface(screen)

        loop_debug(frame, clock, delta)
        await asyncio.sleep(0)


# Entrypoint

if __name__ == "__main__":
    main_entrypoint(run_loop(start_main_loop))
