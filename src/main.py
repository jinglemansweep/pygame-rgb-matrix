import asyncio
import os
import pygame
import pygame.pkgdata
import sys
import traceback
import time
from contextlib import AsyncExitStack
from mqtt_hass_base.daemon import MqttClientDaemon
from pygame.locals import QUIT

sys.path.append(
    os.path.abspath(
        os.path.dirname(__file__) + "/../lib/rpi-rgb-led-matrix/bindings/python"
    )
)

from config import (
    matrix_options,
    LED_ENABLED,
    MQTT_HOST,
    MQTT_PORT,
    MQTT_USER,
    MQTT_PASSWORD,
)
from utils.helpers import (
    render_pygame,
    build_pygame_screen,
    setup_mqtt_client,
)
from theme import Theme

matrix = None
if LED_ENABLED:
    from rgbmatrix import RGBMatrix

    matrix = RGBMatrix(options=matrix_options)

mqtt = setup_mqtt_client()

pygame.init()
screen = build_pygame_screen()
clock = pygame.time.Clock()

theme = Theme()
frame = 0


class Daemon(MqttClientDaemon):
    def read_config(self) -> None:
        pass

    async def _init_main_loop(self, stack: AsyncExitStack) -> None:
        pass

    async def _main_loop(self, stack: AsyncExitStack):
        global camera, frame, screen
        # events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        # frame start
        now = time.localtime()
        screen.fill((0, 0, 0))
        # updates
        theme.update(frame)
        # blitting
        theme.blit(screen)
        # rendering
        render_pygame(screen, matrix)
        # frame end
        clock.tick(120)
        frame += 1


daemon = Daemon("rgbmatrix", MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASSWORD)

asyncio.run(daemon.async_run())
