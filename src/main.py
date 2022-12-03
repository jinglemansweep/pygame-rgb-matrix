import asyncio
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
from pygame.locals import QUIT, RESIZABLE, SCALED

from config import matrix_options, LED_ENABLED, LED_ROWS, LED_COLS
from sprites import BaseSprite
from utils import (
    build_random_color,
    render_pygame,
    build_pygame_screen,
    setup_mqtt_client,
)


COLOR = (255, 255, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_YELLOW_DARK = (31, 31, 31)
COLOR_MAGENTA = (255, 0, 255)
COLOR_MAGENTA_DARK = (63, 0, 63)
COLOR_GREY = (127, 127, 127)
COLOR_GREY_DARK = (15, 15, 15)
COLOR_WHITE = (255, 255, 255)
COLOR_BACKGROUND = (0, 0, 0)

matrix = None
if LED_ENABLED:
    from rgbmatrix import RGBMatrix

    matrix = RGBMatrix(options=matrix_options)


mqtt = setup_mqtt_client()

pygame.init()
screen = build_pygame_screen()
clock = pygame.time.Clock()
font_small = pygame.font.SysFont(None, 14)
font_medium = pygame.font.SysFont(None, 24)
font_large = pygame.font.SysFont(None, 80)

root = pygame.sprite.Group()

actors = pygame.sprite.Group()
for i in range(3, random.randint(3, 100)):
    s = BaseSprite(random.randint(1, 3), random.randint(1, 3), build_random_color(63))
    s.rect.x = random.randint(0, LED_COLS)
    s.rect.y = random.randint(0, LED_ROWS)
    actors.add(s)
root.add(actors)

x = 0
y = 0
frame = 0


def run():
    print("start asyncio event loop")

    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            print("EXCEPTION", e)
        finally:
            print(f"asyncio restarting")
            time.sleep(1)
            asyncio.new_event_loop()


async def main():
    mqtt.loop_start()
    while True:
        await asyncio.create_task(tick())
        await asyncio.sleep(0.001)


async def tick():
    global frame
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
    root.draw(screen)
    t_frame = font_small.render(f"{frame}", True, COLOR_YELLOW_DARK)
    screen.blit(t_frame, (LED_COLS - 24, 0))
    t_hiss = font_large.render("PARTY!", True, COLOR_MAGENTA_DARK)
    screen.blit(
        pygame.transform.rotozoom(t_hiss, frame % 360, 1 * (frame % 1000) / 1000),
        (0, 0),
    )
    t_ss = font_large.render("{:0>2d}".format(now.tm_sec), True, COLOR_GREY_DARK)
    screen.blit(
        pygame.transform.rotozoom(t_ss, frame % 360, 1 * (frame % 100) / 100), (0, 0)
    )
    t_hhmm = font_medium.render(
        "{:0>2d}:{:0>2d}".format(now.tm_hour, now.tm_min), True, COLOR_GREY
    )
    screen.blit(
        t_hhmm,
        (10, 10),
    )
    render_pygame(screen, matrix)
    clock.tick(60)
    frame += 1


run()
