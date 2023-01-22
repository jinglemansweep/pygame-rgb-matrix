import logging
import numpy as np
import pygame
import random
from PIL import Image


def setup_logger(debug=False):
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)


def render_led_matrix(screen, matrix=None):
    if not matrix:
        return
    image_array = pygame.surfarray.array3d(screen)
    image_array = np.rot90(image_array, 1)
    image_array = np.flip(image_array, 0)
    image_rgb = Image.fromarray(image_array, mode="RGB")
    matrix.SetImage(image_rgb)


def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


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
