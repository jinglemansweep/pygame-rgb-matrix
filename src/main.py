import logging
import math
import os
import pygame
import pygame.pkgdata
import random
import sys
import time
import uuid
from argparse import ArgumentParser
from pygame.locals import QUIT, RESIZABLE, SCALED


sys.path.append(
    os.path.abspath(
        os.path.dirname(__file__) + "/../lib/rpi-rgb-led-matrix/bindings/python"
    )
)

from config import (
    matrix_options,
    LED_ENABLED,
    LED_CHAIN,
    LED_PARALLEL,
    LED_ROWS,
    LED_COLS,
    PANEL_ROWS,
    PANEL_COLS,
)
from utils.helpers import (
    random_color,
    render_led_matrix,
    setup_logger,
    JoyPad,
)

_APP_NAME = "wideboy"
_APP_DESCRIPTION = "WideBoy RGB Matrix Platform"
_APP_VERSION = "0.0.1"

parser = ArgumentParser(description=f"{_APP_DESCRIPTION} v{_APP_VERSION}")
parser.add_argument("-v", "--verbose", action="store_true")

args = parser.parse_args()
setup_logger(debug=args.verbose)
logger = logging.getLogger("main")

device_id = uuid.getnode()

pygame.init()
clock = pygame.time.Clock()
font_large = pygame.font.SysFont(None, 96)
# pygame.event.set_allowed([QUIT])
pygame.display.set_caption(_APP_DESCRIPTION)
screen_flags = RESIZABLE | SCALED
screen = pygame.display.set_mode(
    (LED_COLS * PANEL_COLS, LED_ROWS * PANEL_ROWS), screen_flags, 16
)

logger.info(f"RGB Matrix")
logger.info(f"Panel Dimensions:  {LED_COLS}px x {LED_ROWS}px")
logger.info(f"Wall Dimensions:   {PANEL_COLS*LED_COLS}px x {PANEL_ROWS*LED_ROWS}px")
logger.info(f"Wall Layout:       {PANEL_COLS} x {PANEL_ROWS} (panels)")
logger.info(
    f"GUI Dimensions:    {LED_COLS*LED_CHAIN}px x {LED_ROWS*LED_PARALLEL}px",
)


# joypad = JoyPad(0)

LED_ENABLED = True

matrix = None
if LED_ENABLED:
    from rgbmatrix import RGBMatrix

    matrix = RGBMatrix(options=matrix_options)


frame = 0


class Square(pygame.sprite.Sprite):
    def __init__(self, x, y, index, width=64, height=64, color=None):
        super().__init__()
        self.width = width
        self.height = height
        self.index = index
        self.color = color or random_color()
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y

    def update(self, frame):
        self.image = pygame.Surface([self.width, self.height])
        pygame.draw.rect(
            self.image,
            self.color,
            pygame.Rect(0, 0, self.width, self.height),
        )
        step = frame * 0.1
        step %= 2 * math.pi
        frame_sine = -1 * math.sin(step) * 1
        text_offset = (10, 1)
        text_label_shadow = font_large.render(
            self._build_label(self.index), True, (0, 0, 0)
        )
        text_label = font_large.render(
            self._build_label(self.index), True, (255, 255, 255)
        )
        scale = 0.9 + (frame_sine * 0.1)
        rotation = frame_sine * 5
        self.image.blit(
            pygame.transform.rotozoom(text_label_shadow, rotation, scale),
            (text_offset[0] + 2, text_offset[1] + 2),
        )
        self.image.blit(
            pygame.transform.rotozoom(text_label, rotation, scale),
            (text_offset[0], text_offset[1]),
        )

    def _build_label(self, index):
        return f"{index}"


def run():
    global frame

    px = 0
    py = 0

    sprites_panels = pygame.sprite.Group()

    for pi in range(0, PANEL_ROWS * PANEL_COLS):
        for pc in range(0, PANEL_COLS):
            sprites_panels.add(
                Square(px, py, index=pc, width=LED_COLS, height=LED_ROWS)
            )
            px += LED_COLS
            if px >= LED_COLS * PANEL_COLS:
                px = 0
                py += LED_ROWS

    while True:
        for event in pygame.event.get():
            # joypad.process_event(event)
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill((0, 0, 0))
        sprites_panels.update(frame)
        sprites_panels.draw(screen)
        render_led_matrix(screen, matrix)
        pygame.display.flip()
        # clock.tick(30)
        time.sleep(0.005)
        frame += 1


if __name__ == "__main__":
    run()
