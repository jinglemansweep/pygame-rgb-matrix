import asyncio
import cProfile
import logging
import pygame
import sys
import traceback
from pygame import QUIT, DOUBLEBUF, RESIZABLE, SCALED

from wideboy.config import LED_ROWS, LED_COLS, PANEL_ROWS, PANEL_COLS, PROFILING


def setup_pygame(description):

    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption(description)
    screen = pygame.display.set_mode(
        (LED_COLS * PANEL_COLS, LED_ROWS * PANEL_ROWS), RESIZABLE | SCALED | DOUBLEBUF
    )
    return clock, screen


def handle_event(event):
    if event.type == QUIT:
        sys.exit()


def main_entrypoint(main_func):
    if PROFILING in ["ncalls", "tottime"]:
        cProfile.run("main_func()", None, sort=PROFILING)
    else:
        main_func()


def run_loop(loop_func):
    while True:
        try:
            asyncio.run(loop_func())
        except Exception as e:
            logging.error(traceback.format_exc())
