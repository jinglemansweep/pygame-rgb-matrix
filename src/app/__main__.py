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
    IMAGE_PATH,
)

# from app.utils.clock import ClockWidget
from app.utils.images import ImageWidget
from app.utils.ticker import TickerWidget

from app.sprites.clock import ClockWidgetSprite
from app.sprites.ticker import TickerWidgetSprite
from app.sprites.utils.images import glob_files, load_and_resize_image

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
    screen_flags |= RESIZABLE | SCALED

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
matrix_buffer = None
matrix_surface = None
if LED_ENABLED:
    from rgbmatrix import RGBMatrix

    matrix = RGBMatrix(options=matrix_options)
    matrix_buffer = matrix.CreateFrameCanvas()
    matrix_surface = pygame.Surface(
        (LED_COLS * LED_CHAIN, LED_ROWS * LED_PARALLEL), depth=PYGAME_BITS_PER_PIXEL
    )

frame = 0


async def _update_ticker(loop, ticker, url, interval):
    feed = await get_rss_items(loop, url)
    now = datetime.now()
    time_fmt = now.strftime("%H:%M")
    header = f"Latest News @ {time_fmt}"
    ticker.add_text_item(header)
    entries = feed.entries
    for idx, item in enumerate(entries):
        ticker.add_text_item(html.unescape(item["title"]))
    ticker.render_surface()
    logger.info(f"rss:fetch url={url} entries={len(entries)} interval={interval}")
    await asyncio.sleep(interval)
    asyncio.create_task(_update_ticker(loop, ticker, url, interval))


async def start_main_loop():

    global frame, matrix, matrix_surface, matrix_buffer

    mqtt.loop_start()

    background = pygame.Surface(
        (LED_COLS * PANEL_COLS, LED_ROWS * PANEL_ROWS), 0, PYGAME_BITS_PER_PIXEL
    )
    background.fill((0, 0, 32, 255))
    sprites = pygame.sprite.LayeredDirty(background=background)

    sprite_images = TickerWidgetSprite(
        ((0, 0, LED_COLS * PANEL_COLS, LED_ROWS * PANEL_ROWS)),
        item_margin=16,
        scroll_speed=0.1,
    )
    sprites.add(sprite_images)

    sprite_ticker = TickerWidgetSprite(
        (0, 40, LED_COLS * PANEL_COLS, 24), item_margin=100
    )
    sprites.add(sprite_ticker)

    sprite_clock = ClockWidgetSprite(
        (LED_COLS * (PANEL_COLS - 2), 0, LED_COLS * 2, LED_ROWS * PANEL_ROWS),
        color_bg=(128, 0, 0, 192),
    )
    sprites.add(sprite_clock)

    image_path = os.path.join("..", IMAGE_PATH)
    images = glob_files(image_path, "*.jpg")
    for image_filename in images[:3]:
        sprite_images.add_image_item(image_filename, (LED_COLS * 2, LED_ROWS))
    sprite_images.render_surface()

    loop = asyncio.get_event_loop()
    asyncio.create_task(
        _update_ticker(loop, sprite_ticker, RSS_URL, RSS_UPDATE_INTERVAL)
    )

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

        sprites.update(frame)
        sprites.clear(screen, background)
        update_rects = sprites.draw(screen)
        # logger.debug(f"main:ticker:draw updates={update_rects}")

        if GUI_ENABLED:
            pygame.display.update(update_rects)
        matrix_buffer = render_led_matrix(screen, matrix, matrix_surface, matrix_buffer)

        clock.tick(255)
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
