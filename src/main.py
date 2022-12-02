import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.dirname(__file__) + "/../lib/rpi-rgb-led-matrix/bindings/python"
    )
)

import pygame
import random
from pygame.locals import QUIT
from rgbmatrix import RGBMatrix

from config import matrix_options, LED_ROWS, LED_COLS
from sprites import BaseSprite
from utils import build_random_color, render_pygame_to_matrix

COLOR = (255, 255, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_BACKGROUND = (0, 0, 0)

matrix = RGBMatrix(options=matrix_options)
pygame.init()
screen = pygame.display.set_mode((LED_COLS, LED_ROWS))
clock = pygame.time.Clock()

actors = pygame.sprite.Group()
for i in range(3, random.randint(3, 50)):
    s = BaseSprite(random.randint(1, 3), random.randint(1, 3), build_random_color())
    s.rect.x = random.randint(0, 63)
    s.rect.y = random.randint(0, 63)
    actors.add(s)

x = 0
y = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    for actor in actors:
        # print(actor.rect)
        actor.rect.x += 1
        if actor.rect.x > LED_COLS:
            actor.rect.y += 1
            actor.rect.x = 0
        if actor.rect.y > LED_ROWS:
            actor.rect.y = 0
        actor.update()
    actors.update()
    screen.fill(COLOR_BACKGROUND)
    actors.draw(screen)
    render_pygame_to_matrix(screen, matrix)
    clock.tick(200)
