import html
import logging
import math
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
    LED_CHAIN,
    LED_PARALLEL,
    LED_ROWS,
    LED_COLS,
    PANEL_ROWS,
    PANEL_COLS,
    MQTT_HOST,
    MQTT_PORT,
    MQTT_USER,
    MQTT_PASSWORD,
    DEVICE_NAME,
)
from utils.background import Background
from utils.clock import ClockWidget
from utils.ticker import TickerWidget
from utils.hass import HASSManager, setup_mqtt_client
from utils.helpers import (
    get_rss_items,
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

mqtt = setup_mqtt_client(MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASSWORD)
hass = HASSManager(mqtt, DEVICE_NAME, _APP_NAME)
hass.add_entity("power", "Power", "switch", {}, dict(state="ON"))
hass.add_entity("show_date", "Show Date", "switch", {}, dict(state="ON"))


def _on_message(client, userdata, msg):
    hass.process_message(str(msg.topic), str(msg.payload))


mqtt.on_message = _on_message

pygame.init()
clock = pygame.time.Clock()
font_large = pygame.font.SysFont(None, 96)
font_tiny = pygame.font.SysFont(None, 16)
# pygame.event.set_allowed([QUIT])
pygame.display.set_caption(_APP_DESCRIPTION)
screen_flags = RESIZABLE | SCALED

screen = pygame.display.set_mode(
    (LED_COLS * PANEL_COLS, LED_ROWS * PANEL_ROWS), screen_flags, 16
)

logger.info(f"RGB Matrix")
logger.info(f"Panel Dimensions:  {LED_COLS}px x {LED_ROWS}px")
logger.info(f"Wall Dimensions:   {PANEL_COLS*LED_COLS}px x {PANEL_ROWS*LED_ROWS}px")
logger.info(f"Wall Layout:       {PANEL_COLS} x {PANEL_ROWS} (panels)")
logger.info(
    f"GUI Dimensions:    {LED_COLS*LED_CHAIN}px x {LED_ROWS*LED_PARALLEL}px",
)


# joypad = JoyPad(0)

LED_ENABLED = True

matrix = None
if LED_ENABLED:
    from rgbmatrix import RGBMatrix

    matrix = RGBMatrix(options=matrix_options)


frame = 0

NEWS_RSS_URL = "https://feeds.skynews.com/feeds/rss/home.xml"
WOTD_RSS_URL = "https://www.oed.com/rss.xml"


def run():
    global frame

    mqtt.loop_start()

    sprites = pygame.sprite.Group()

    background = Background((0, 0, LED_COLS * PANEL_COLS, LED_ROWS * PANEL_ROWS))
    clock_widget = ClockWidget(
        (LED_COLS * (PANEL_COLS - 2), 0, LED_COLS * 2, LED_ROWS * PANEL_ROWS),
        color_bg=(128, 0, 0, 255),
    )
    ticker = TickerWidget(
        (0, 0, LED_COLS * PANEL_COLS, 40),
        color_bg=(0, 0, 128, 255),
        font_size=34,
        scroll_speed=2,
    )
    ticker_alt = TickerWidget(
        (0, 40, LED_COLS * PANEL_COLS, 24),
        color_bg=(255, 255, 255, 255),
        color_fg=(0, 0, 0, 255),
        font_size=18,
        scroll_speed=1,
        padding=0,
        item_margin=30,
    )

    # Z-Order
    sprites.add(background)
    sprites.add(ticker)
    sprites.add(ticker_alt)
    sprites.add(clock_widget)

    news = get_rss_items(NEWS_RSS_URL)
    for item in news.entries:
        ticker.add(html.unescape(item["title"]))

    wotd = get_rss_items(WOTD_RSS_URL)
    for item in wotd.entries:
        title = str(item["description"]).replace("OED Word of the Day: ", "")
        ticker_alt.add(html.unescape(title))

    while True:
        for event in pygame.event.get():
            # joypad.process_event(event)
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill((0, 0, 0))

        if hass.store["power"].state["state"] == "ON":
            sprites.update(frame)
            sprites.draw(screen)

        """
        if frame % 5000 == 100:
            clock_widget.set_mode("hiding")
        if frame % 5000 == 500:
            clock_widget.set_mode("showing")
        """

        render_led_matrix(screen, matrix)
        pygame.display.flip()
        clock.tick(120)
        frame += 1


if __name__ == "__main__":
    run()
