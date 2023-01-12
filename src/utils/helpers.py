import asyncio
import logging
import pygame
import random
import sys
from PIL import Image
from pygame.locals import QUIT, RESIZABLE, SCALED, BLEND_RGBA_ADD

from config import VIRTUAL_SCREEN_SIZE

EVDEV_KEY_ESCAPE = 1
EVDEV_KEY_CURSOR_UP = 103
EVDEV_KEY_CURSOR_DOWN = 108
EVDEV_KEY_CURSOR_LEFT = 105
EVDEV_KEY_CURSOR_RIGHT = 106
EVDEV_KEY_SPACE = 57
EVDEV_KEY_A = 30
EVDEV_KEY_D = 32

EVDEV_GAMEPAD_DPAD_X = 16
EVDEV_GAMEPAD_DPAD_Y = 17
EVDEV_GAMEPAD_CROSS = 304
EVDEV_GAMEPAD_CIRCLE = 305
EVDEV_GAMEPAD_SQUARE = 307
EVDEV_GAMEPAD_TRIANGLE = 308
EVDEV_GAMEPAD_L1 = 310
EVDEV_GAMEPAD_R1 = 311
EVDEV_GAMEPAD_L2 = 312
EVDEV_GAMEPAD_R2 = 313
EVDEV_GAMEPAD_SELECT = 314
EVDEV_GAMEPAD_START = 315
EVDEV_GAMEPAD_L3 = 317
EVDEV_GAMEPAD_R3 = 318


def setup_logger(debug=False):
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)


def build_pygame_screen():
    pygame.display.set_caption("RGB MATRIX")
    return pygame.display.set_mode(VIRTUAL_SCREEN_SIZE, 16)


def render_pygame(screen, matrix=None):
    if matrix is not None:
        flipped = pygame.transform.flip(screen, True, False)
        screen.blit(
            flipped,
            (0, 0),
        )
        imgdata = pygame.surfarray.array3d(screen)
        image_rgb = Image.fromarray(imgdata, mode="RGB")
        matrix.SetImage(image_rgb)
    pygame.display.flip()


def build_context(frame, screen, joypad):
    return (frame, screen, joypad)


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
