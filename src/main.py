import cProfile
import html
import logging
import os
import pygame
import pygame.pkgdata
import sys
from argparse import ArgumentParser
from pygame.locals import QUIT, FULLSCREEN, DOUBLEBUF


sys.path.append(
    os.path.abspath(
        os.path.dirname(__file__) + "/../lib/rpi-rgb-led-matrix/bindings/python"
    )
)

from config import (
    matrix_options,
    DEBUG,
    GUI_ENABLED,
    PYGAME_FPS,
    PYGAME_BITS_PER_PIXEL,
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
from utils.hass import HASSManager, setup_mqtt_client, OPTS_LIGHT_RGB
from utils.helpers import (
    get_rss_items,
    hass_to_color,
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
setup_logger(debug=DEBUG or args.verbose)
logger = logging.getLogger("main")

mqtt = setup_mqtt_client(MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASSWORD)
hass = HASSManager(mqtt, DEVICE_NAME, _APP_NAME)
hass.add_entity("power", "Power", "switch", {}, dict(state="ON"))
hass.add_entity("show_background", "Show Background", "switch", {}, dict(state="ON"))
hass.add_entity("show_clock", "Show Clock", "switch", {}, dict(state="ON"))
hass.add_entity("show_news", "Show News", "switch", {}, dict(state="ON"))
hass.add_entity("show_updates", "Show Updates", "switch", {}, dict(state="ON"))
hass.add_entity(
    "color_clock",
    "Clock Color",
    "light",
    OPTS_LIGHT_RGB,
    dict(state="ON", color=dict(r=0x90, g=0x00, b=0x00), brightness=255),
)
hass.add_entity(
    "color_news",
    "News Color",
    "light",
    OPTS_LIGHT_RGB,
    dict(state="ON", color=dict(r=0x00, g=0x00, b=0x90), brightness=255),
)
hass.add_entity(
    "color_updates",
    "Updates Color",
    "light",
    OPTS_LIGHT_RGB,
    dict(state="ON", color=dict(r=0xFF, g=0xFF, b=0xFF), brightness=255),
)


def _on_message(client, userdata, msg):
    hass.process_message(msg.topic, msg.payload.decode("UTF-8"))


mqtt.on_message = _on_message

pygame.init()
clock = pygame.time.Clock()
pygame.event.set_allowed([QUIT])
pygame.display.set_caption(_APP_DESCRIPTION)

screen = pygame.display.set_mode(
    (LED_COLS * PANEL_COLS, LED_ROWS * PANEL_ROWS),
    FULLSCREEN | DOUBLEBUF,
    PYGAME_BITS_PER_PIXEL,
)

logger.info(f"RGB Matrix")
logger.info(f"Panel Dimensions:  {LED_COLS}px x {LED_ROWS}px")
logger.info(f"Wall Dimensions:   {PANEL_COLS*LED_COLS}px x {PANEL_ROWS*LED_ROWS}px")
logger.info(f"Wall Layout:       {PANEL_COLS} x {PANEL_ROWS} (panels)")
logger.info(
    f"GUI Dimensions:    {LED_COLS*LED_CHAIN}px x {LED_ROWS*LED_PARALLEL}px",
)

# joypad = JoyPad(0)

matrix = None
double_buffer = None
if LED_ENABLED:
    from rgbmatrix import RGBMatrix

    matrix = RGBMatrix(options=matrix_options)
    double_buffer = matrix.CreateFrameCanvas()

frame = 0

NEWS_RSS_URL = "https://feeds.skynews.com/feeds/rss/home.xml"
WOTD_RSS_URL = "https://www.oed.com/rss.xml"
HN_RSS_URL = "https://hnrss.org/frontpage"


def loop():
    global frame, double_buffer

    mqtt.loop_start()

    sprites = pygame.sprite.Group()

    background = Background((0, 0, LED_COLS * PANEL_COLS, LED_ROWS * PANEL_ROWS))
    clock_widget = ClockWidget(
        (LED_COLS * (PANEL_COLS - 2), 0, LED_COLS * 2, LED_ROWS * PANEL_ROWS),
        color_bg=(128, 0, 0, 128),
    )
    ticker = TickerWidget(
        (0, 0, LED_COLS * PANEL_COLS, 40),
        color_bg=(0, 0, 128, 128),
        font_size=34,
        scroll_speed=2,
    )
    ticker_alt = TickerWidget(
        (0, 40, LED_COLS * PANEL_COLS, 24),
        color_bg=(255, 255, 255, 196),
        color_fg=(0, 0, 0, 255),
        font_size=18,
        scroll_speed=1,
        padding=0,
        item_margin=30,
    )

    # Z-order
    sprites.add(background)
    sprites.add(ticker)
    sprites.add(ticker_alt)
    sprites.add(clock_widget)

    news = get_rss_items(NEWS_RSS_URL)
    for item in news.entries:
        ticker.add(html.unescape(item["title"]))

    updates = get_rss_items(HN_RSS_URL)
    for item in updates.entries:
        title = str(item["title"])
        # title = str(item["description"]).replace("OED Word of the Day: ", "")
        ticker_alt.add(html.unescape(title))

    while True:
        for event in pygame.event.get():
            # joypad.process_event(event)
            if event.type == pygame.QUIT:
                sys.exit()

        clock_widget.color_bg = hass_to_color(
            hass.store["color_clock"].state["color"],
            hass.store["color_clock"].state["brightness"],
        )
        ticker.color_bg = hass_to_color(
            hass.store["color_news"].state["color"],
            hass.store["color_news"].state["brightness"],
        )
        ticker_alt.color_bg = hass_to_color(
            hass.store["color_updates"].state["color"],
            hass.store["color_updates"].state["brightness"],
        )

        if hass.store["power"].state["state"] == "ON":
            sprites.update(frame)
            if hass.store["show_background"].state["state"] == "ON":
                screen.blit(background.image, background.rect)
            else:
                screen.fill((0, 0, 0))
            if hass.store["show_news"].state["state"] == "ON":
                screen.blit(ticker.image, ticker.rect)
            if hass.store["show_updates"].state["state"] == "ON":
                screen.blit(ticker_alt.image, ticker_alt.rect)
            if hass.store["show_clock"].state["state"] == "ON":
                screen.blit(clock_widget.image, clock_widget.rect)

        if GUI_ENABLED:
            pygame.display.flip()
        double_buffer = render_led_matrix(screen, matrix, double_buffer)

        clock.tick(PYGAME_FPS)

        if frame % 200 == 0:
            logger.info(f"FPS: {clock.get_fps()}")

        frame += 1


def run():
    while True:
        loop()


if __name__ == "__main__":
    cProfile.run("run()", None, sort="ncalls")
