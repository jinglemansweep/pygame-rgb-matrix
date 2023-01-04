import asyncio
import logging
import pygame
import random
import sys
from evdev import InputDevice, KeyEvent, categorize, list_devices, ecodes
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
    return pygame.display.set_mode(VIRTUAL_SCREEN_SIZE, SCALED | RESIZABLE, 32)


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


def build_context(frame, key, screen, hass):
    return (frame, key, screen, hass)


def get_evdev_key(dev):
    if not dev:
        return None
    event = dev.read_one()
    if not event:
        return None
    key = None
    if event.type in (ecodes.EV_KEY, ecodes.EV_ABS):
        key_event = categorize(event)
        code, value = key_event.event.code, key_event.event.value
        print(code, value)
        if code == EVDEV_GAMEPAD_DPAD_X:
            if value < 0:
                key = "left"
            if value > 0:
                key = "right"
        if code == EVDEV_GAMEPAD_DPAD_Y:
            if value < 0:
                key = "up"
            if value > 0:
                key = "down"
        if code == EVDEV_GAMEPAD_CIRCLE:
            key = "circle"
        if code == EVDEV_GAMEPAD_CROSS:
            key = "cross"
        if code == EVDEV_GAMEPAD_SQUARE:
            key = "square"
        if code == EVDEV_GAMEPAD_TRIANGLE:
            key = "triangle"
        if code == EVDEV_GAMEPAD_L1:
            key = "l1"
        if code == EVDEV_GAMEPAD_R1:
            key = "r1"
    return key
