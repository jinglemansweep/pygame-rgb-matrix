import logging
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
# joypad = JoyPad(0)

LED_ENABLED = True

matrix = None
if LED_ENABLED:
    from rgbmatrix import RGBMatrix

    matrix = RGBMatrix(options=matrix_options)


logger.info(f"RGB Matrix")
logger.info(f"Wall Size (panels): rows={PANEL_ROWS} cols={PANEL_COLS}")
logger.info(f"Panel Size (pixels): rows={LED_ROWS} cols={LED_COLS}")
logger.info(
    f"Total Size (pixels): rows={PANEL_ROWS * LED_ROWS} cols={PANEL_COLS * LED_COLS}"
)

frame = 0


class Square(pygame.sprite.Sprite):
    def __init__(self, x, y, width=64, height=64, color=None, label=""):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        pygame.draw.rect(
            self.image,
            color or random_color(),
            pygame.Rect(0, 0, width, height),
        )
        text_offset = (10, 1)
        text_label_shadow = font_large.render(label, True, (0, 0, 0))
        text_label = font_large.render(label, True, (255, 255, 255))
        self.image.blit(text_label_shadow, (text_offset[0] + 2, text_offset[1] + 2))
        self.image.blit(text_label, (text_offset[0], text_offset[1]))
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y


def run():
    global frame

    px = 0
    py = 0

    sprites_panels = pygame.sprite.Group()

    for pi in range(0, PANEL_ROWS * PANEL_COLS):
        for pc in range(0, PANEL_COLS):
            sprites_panels.add(Square(px, py, LED_COLS, LED_ROWS, label=f"{pc}"))
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
        sprites_panels.draw(screen)
        render_led_matrix(screen, matrix)
        pygame.display.flip()
        # clock.tick(30)
        time.sleep(0.005)
        frame += 1


if __name__ == "__main__":
    run()
