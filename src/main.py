import argparse
import os
import pygame
import random
import sys
import time

from PIL import Image
from PIL import ImageDraw
from pygame.locals import QUIT

sys.path.append(
    os.path.abspath(
        os.path.dirname(__file__) + "/../lib/rpi-rgb-led-matrix/bindings/python"
    )
)
from rgbmatrix import RGBMatrix, RGBMatrixOptions

parser = argparse.ArgumentParser()

LED_ROWS = int(os.environ.get("LED_ROWS", 64))
LED_COLS = int(os.environ.get("LED_COLS", 64))
LED_CHAIN = int(os.environ.get("LED_CHAIN", 1))
LED_PARALLEL = int(os.environ.get("LED_PARALLEL", 1))
LED_PWM_BITS = int(os.environ.get("LED_PWM_BITS", 11))
LED_BRIGHTNESS = int(os.environ.get("LED_BRIGHTNESS", 100))
LED_GPIO_MAPPING = os.environ.get("LED_GPIO_MAPPING", None)
LED_SCAN_MODE = int(os.environ.get("LED_SCAN_MODE", 1))
LED_PWM_LSB_NANOSECONDS = int(os.environ.get("LED_PWM_LSB_NANOSECONDS", 130))
LED_SHOW_REFRESH = os.environ.get("LED_SHOW_REFRESH", False)
LED_SLOWDOWN_GPIO = int(os.environ.get("LED_SLOWDOWN_GPIO", 1))
LED_NO_HARDWARE_PULSE = os.environ.get("LED_NO_HARDWARE_PULSE", False)
LED_RGB_SEQUENCE = os.environ.get("LED_RGB_SEQUENCE", "RGB")
LED_PIXEL_MAPPER = os.environ.get("LED_PIXEL_MAPPER", "")
LED_ROW_ADDR_TYPE = int(os.environ.get("LED_ROW_ADDR_TYPE", 0))
LED_MULTIPLEXING = int(os.environ.get("LED_MULTIPLEXING", 0))
LED_PANEL_TYPE  = os.environ.get("LED_PANEL_TYPE", "")

options = RGBMatrixOptions()
if LED_GPIO_MAPPING is not None:
    options.hardware_mapping = LED_GPIO_MAPPING
options.rows = LED_ROWS
options.cols = LED_COLS
options.chain_length = LED_CHAIN
options.parallel = LED_PARALLEL
options.row_address_type = LED_ROW_ADDR_TYPE
options.multiplexing = LED_MULTIPLEXING
options.pwm_bits = LED_PWM_BITS
options.brightness = LED_BRIGHTNESS
options.pwm_lsb_nanoseconds = LED_PWM_LSB_NANOSECONDS
options.led_rgb_sequence = LED_RGB_SEQUENCE
options.pixel_mapper_config = LED_PIXEL_MAPPER
options.panel_type = LED_PANEL_TYPE
options.show_refresh_rate = 1 if LED_SHOW_REFRESH else 0
if LED_SLOWDOWN_GPIO is not None:
    options.gpio_slowdown = LED_SLOWDOWN_GPIO
if LED_NO_HARDWARE_PULSE:
    options.disable_hardware_pulsing = True
options.drop_privileges = True

print(options)

COLOR = (255, 255, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_BACKGROUND = (0, 0, 0)
WIDTH = 64
HEIGHT = 64

matrix = RGBMatrix(options=options)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, w, h, color):
        super().__init__()
        self.image = pygame.Surface([w, h])
        self.image.fill(COLOR_BACKGROUND)
        self.image.set_colorkey(COLOR_BACKGROUND)
        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, w, h))
        self.rect = self.image.get_rect()


def build_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


os.putenv("SDL_VIDEODRIVER", "dummy")
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Hello World!")

x = 0
y = 0

clock = pygame.time.Clock()

actors = pygame.sprite.Group()
for i in range(3, random.randint(3, 50)):
    s = Sprite(random.randint(1, 3), random.randint(1, 3), build_random_color())
    s.rect.x = random.randint(0, 63)
    s.rect.y = random.randint(0, 63)
    actors.add(s)


while True:  # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    for actor in actors:
        #print(actor.rect)
        actor.rect.x += 1
        if actor.rect.x > WIDTH:
            actor.rect.y += 1
            actor.rect.x = 0
        if actor.rect.y > HEIGHT:
            actor.rect.y = 0
        actor.update()
    actors.update()
    screen.fill(COLOR_BACKGROUND)
    actors.draw(screen)
    pygame.display.flip()
    time.sleep(0.01)
    screen.blit(pygame.transform.flip(screen, False, True), dest=(0, 0))
    imgdata = pygame.surfarray.array3d(screen)    
    image_rgb = Image.fromarray(imgdata, mode="RGB")
    matrix.SetImage(image_rgb)
    clock.tick(200)
