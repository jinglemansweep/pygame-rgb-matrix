import asyncio
import cProfile
import logging
import pygame
import sys
import traceback
from pygame import QUIT, DOUBLEBUF, RESIZABLE, SCALED
from typing import Callable

from wideboy.config import (
    PYGAME_FPS,
    PROFILING,
)

logger = logging.getLogger(__name__)

frame = 0


def setup_pygame(
    display_size: tuple[int, int], caption: str
) -> tuple[pygame.time.Clock, pygame.surface.Surface]:

    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption(caption)
    screen = pygame.display.set_mode(display_size, RESIZABLE | SCALED | DOUBLEBUF)
    return clock, screen


def handle_event(event: pygame.event.Event) -> None:
    if event.type == QUIT:
        sys.exit()


function


def main_entrypoint(main_func: Callable) -> None:
    if PROFILING in ["ncalls", "tottime"]:
        cProfile.run("main_func()", None, sort=PROFILING)
    else:
        main_func()


def run_loop(loop_func: Callable) -> None:
    while True:
        try:
            asyncio.run(loop_func())
        except Exception as e:
            logging.error(traceback.format_exc())


def loop_debug(
    frame: int, clock: pygame.time.Clock, delta: float, every: int = 200
) -> None:
    if frame % every == 0:
        logger.info(f"debug:loop frame={frame} fps={clock.get_fps()} delta={delta}")


def clock_tick(clock: pygame.time.Clock) -> tuple[int, float]:
    global frame
    delta = clock.tick(PYGAME_FPS) / 1000
    frame += 1
    return frame, delta
