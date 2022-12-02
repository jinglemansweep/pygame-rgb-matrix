import os
import sys
import time

sys.path.append(
    os.path.abspath(
        os.path.dirname(__file__) + "/../lib/rpi-rgb-led-matrix/bindings/python"
    )
)

import pygame
import random
from pygame.locals import QUIT, RESIZABLE

from config import matrix_options, LED_ENABLED, LED_ROWS, LED_COLS
from sprites import BaseSprite
from utils import build_random_color, render_pygame


COLOR = (255, 255, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_GREY = (127, 127, 127)
COLOR_WHITE = (255, 255, 255)
COLOR_BACKGROUND = (0, 0, 0)

matrix = None
if LED_ENABLED:
    from rgbmatrix import RGBMatrix

    matrix = RGBMatrix(options=matrix_options)


pygame.init()
pygame.display.set_caption("RGB MATRIX")
screen = pygame.display.set_mode((LED_COLS, LED_ROWS))
clock = pygame.time.Clock()
font_small = pygame.font.SysFont(None, 14)
font_medium = pygame.font.SysFont(None, 24)
font_large = pygame.font.SysFont(None, 40)

root = pygame.sprite.Group()

actors = pygame.sprite.Group()
for i in range(3, random.randint(3, 100)):
    s = BaseSprite(random.randint(1, 3), random.randint(1, 3), build_random_color())
    s.rect.x = random.randint(0, LED_COLS)
    s.rect.y = random.randint(0, LED_ROWS)
    actors.add(s)
root.add(actors)


x = 0
y = 0
frame = 0

while True:
    now = time.localtime()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    for actor in actors:
        actor.rect.x += 1
        if actor.rect.x > LED_COLS:
            actor.rect.y += 1
            actor.rect.x = 0
        if actor.rect.y > LED_ROWS:
            actor.rect.y = 0
    actors.update()
    screen.fill(COLOR_BACKGROUND)
    t_frame = font_small.render(f"{frame}", True, COLOR_YELLOW)
    screen.blit(t_frame, (0, 0))
    t_hhmm = font_medium.render(
        "{}:{}".format(now.tm_hour, now.tm_min), True, COLOR_GREY
    )
    screen.blit(t_hhmm, (0, 10))
    t_ss = font_large.render("{}".format(now.tm_sec), True, COLOR_GREY)
    screen.blit(t_ss, (30, 20))
    root.draw(screen)
    render_pygame(screen, matrix)

    clock.tick(200)
    frame += 1
