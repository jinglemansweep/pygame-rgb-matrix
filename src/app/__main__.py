import asyncio
import cProfile
import html
import json
import logging
import os
import pygame
import pygame.pkgdata
import sys
import traceback

from argparse import ArgumentParser
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from pygame.locals import QUIT, DOUBLEBUF, RESIZABLE, SCALED

load_dotenv(find_dotenv())

sys.path.append(
    os.path.abspath(
        os.path.dirname(__file__) + "/../../lib/rpi-rgb-led-matrix/bindings/python"
    )
)

from app.config import (
    matrix_options,
    DEBUG,
    PROFILING,
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
    RSS_URL,
    RSS_UPDATE_INTERVAL,
    MQTT_HOST,
    MQTT_PORT,
    MQTT_USER,
    MQTT_PASSWORD,
    DEVICE_NAME,
)
from app.utils.background import Background
from app.utils.clock import ClockWidget
from app.utils.ticker import TickerWidget
from app.utils.hass import HASSManager, setup_mqtt_client, OPTS_LIGHT_RGB
from app.utils.helpers import (
    get_rss_items,
    hass_to_color,
    hass_to_visible,
    render_led_matrix,
    setup_logger,
    JoyPad,
)

_APP_NAME = "wideboy"
_APP_DESCRIPTION = "WideBoy RGB Matrix Platform"
_APP_VERSION = "0.0.1"

MQTT_MESSAGE_RECEIVED = pygame.USEREVENT + 1

parser = ArgumentParser(description=f"{_APP_DESCRIPTION} v{_APP_VERSION}")
parser.add_argument("-v", "--verbose", action="store_true")

args = parser.parse_args()
setup_logger(debug=DEBUG or args.verbose)
logger = logging.getLogger("main")

mqtt = setup_mqtt_client(MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASSWORD)
hass = HASSManager(mqtt, DEVICE_NAME, _APP_NAME)
hass.add_entity("power", "Power", "switch", {}, dict(state="ON"))
hass.add_entity("show_background", "Show Background", "switch", {}, dict(state="ON"))
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
    "command_test", "Command", "text", dict(mode="text"), dict(text="HELLO")
)


def _on_message(client, userdata, msg):
    payload = msg.payload.decode("UTF-8")
    pygame.event.post(
        pygame.event.Event(MQTT_MESSAGE_RECEIVED, topic=msg.topic, message=payload)
    )


mqtt.on_message = _on_message


pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption(_APP_DESCRIPTION)

screen_flags = DOUBLEBUF
if GUI_ENABLED:
    screen_flags |= SCALED | RESIZABLE

screen = pygame.display.set_mode(
    (LED_COLS * PANEL_COLS, LED_ROWS * PANEL_ROWS),
    screen_flags,
    PYGAME_BITS_PER_PIXEL,
)

logger.info(f"{_APP_DESCRIPTION} v{_APP_VERSION}")
logger.info(f"panel:size w={LED_COLS}px h={LED_ROWS}px")
logger.info(f"wall:size: w={PANEL_COLS*LED_COLS}px h={PANEL_ROWS*LED_ROWS}px")
logger.info(f"wall:layout w={PANEL_COLS} h={PANEL_ROWS}")
logger.info(
    f"gui:size w={LED_COLS*LED_CHAIN}px h={LED_ROWS*LED_PARALLEL}px",
)

# joypad = JoyPad(0)

matrix = None
double_buffer = None
if LED_ENABLED:
    from rgbmatrix import RGBMatrix

    matrix = RGBMatrix(options=matrix_options)
    double_buffer = matrix.CreateFrameCanvas()

frame = 0


async def _update_ticker(loop, ticker, url, interval):
    ticker.expire_all()
    feed = await get_rss_items(loop, url)
    now = datetime.now()
    time_fmt = now.strftime("%H:%M")
    header = f"Latest News @ {time_fmt}"
    ticker.add(header)
    entries = feed.entries
    for idx, item in enumerate(entries):
        # ticker.add(f"idx {idx}", transient=True)
        ticker.add(html.unescape(item["title"]))
    logger.info(f"rss:fetch url={url} entries={len(entries)} interval={interval}")
    await asyncio.sleep(interval)
    asyncio.create_task(_update_ticker(loop, ticker, url, interval))


async def start_main_loop():

    global frame, double_buffer

    mqtt.loop_start()

    sprites = pygame.sprite.LayeredDirty()

    background = Background((0, 0, LED_COLS * PANEL_COLS, LED_ROWS * PANEL_ROWS))
    clock_widget = ClockWidget(
        (LED_COLS * (PANEL_COLS - 2), 0, LED_COLS * 2, LED_ROWS * PANEL_ROWS),
        color_bg=(128, 0, 0, 128),
    )
    ticker = TickerWidget(
        (0, 40, LED_COLS * PANEL_COLS, 24),
        color_bg=(0, 0, 0, 128),
        font_size=20,
    )

    # Z-order
    sprites.add(background)
    sprites.add(ticker)
    sprites.add(clock_widget)

    loop = asyncio.get_event_loop()
    asyncio.create_task(_update_ticker(loop, ticker, RSS_URL, RSS_UPDATE_INTERVAL))

    while True:
        for event in pygame.event.get():
            # joypad.process_event(event)
            if event.type == QUIT:
                sys.exit()
            if event.type == MQTT_MESSAGE_RECEIVED:
                logger.info(
                    f"mqtt:message: topic={event.topic} message={event.message}"
                )
                hass.process_message(event.topic, event.message)

        clock_widget.color_bg = hass_to_color(
            hass.store["color_clock"].state["color"],
            hass.store["color_clock"].state["brightness"],
        )

        # ticker.color_bg = hass_to_color(
        #     hass.store["color_news"].state["color"],
        #     hass.store["color_news"].state["brightness"],
        # )

        switch_master = hass.store["power"].state["state"] == "ON"
        switch_background = hass.store["show_background"].state["state"] == "ON"
        color_clock = hass.store["color_clock"].state["state"] == "ON"
        color_ticker = hass.store["color_news"].state["state"] == "ON"

        if not switch_background:
            screen.fill((0, 0, 0))
        background.visible = hass_to_visible(switch_background, switch_master)
        clock_widget.visible = hass_to_visible(color_clock, switch_master)
        ticker.visible = hass_to_visible(color_ticker, switch_master)

        sprites.update(frame)
        sprites.draw(screen)

        if GUI_ENABLED:
            pygame.display.flip()
        double_buffer = render_led_matrix(screen, matrix, double_buffer)

        clock.tick(PYGAME_FPS)
        await asyncio.sleep(0)

        if frame % 200 == 0:
            logger.info(f"debug:clock fps={clock.get_fps()}")

        frame += 1


def run():
    while True:
        try:
            asyncio.run(start_main_loop())
        except Exception as e:
            logging.error(traceback.format_exc())


if __name__ == "__main__":
    if PROFILING in ["ncalls", "tottime"]:
        cProfile.run("run()", None, sort=PROFILING)
    else:
        run()
