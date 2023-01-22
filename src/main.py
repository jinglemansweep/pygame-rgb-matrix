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

from config import matrix_options, LED_ENABLED, LED_LIMIT_REFRESH, VIRTUAL_SCREEN_SIZE
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
# pygame.event.set_allowed([QUIT])
pygame.display.set_caption(_APP_DESCRIPTION)
screen_flags = RESIZABLE | SCALED
screen = pygame.display.set_mode(VIRTUAL_SCREEN_SIZE, screen_flags, 16)
# joypad = JoyPad(0)

LED_ENABLED = True

matrix = None
if LED_ENABLED:
    from rgbmatrix import RGBMatrix

    matrix = RGBMatrix(options=matrix_options)


frame = 0


class Square(pygame.sprite.Sprite):
    def __init__(self, x, y, width=8, height=32, color=None):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        pygame.draw.rect(
            self.image,
            color or random_color(),
            pygame.Rect(0, 0, width, height),
        )
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y
        self.speed = 2.0

    def update(self, frame):
        self.rect[0] -= self.speed
        if self.rect[0] < 1:
            self.rect[0] = 600


def run():
    global frame

    sprites = pygame.sprite.Group()
    for i in range(0, 40):
        sprites.add(Square(500 + (i * 20), 10))

    while True:
        for event in pygame.event.get():
            # joypad.process_event(event)
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill((0, 0, 0))
        sprites.update(frame)
        sprites.draw(screen)
        render_led_matrix(screen, matrix)
        pygame.display.flip()
        # clock.tick(30)
        time.sleep(0.005)
        frame += 1


if __name__ == "__main__":
    run()
