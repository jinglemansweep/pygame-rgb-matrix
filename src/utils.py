import pygame
import random
import paho.mqtt.client as mqtt
from PIL import Image
from pygame.locals import QUIT, RESIZABLE, SCALED, BLEND_RGBA_ADD

from config import (
    LED_ENABLED,
    GUI_ENABLED,
    LED_COLS,
    LED_ROWS,
    MQTT_HOST,
    MQTT_PORT,
    MQTT_USER,
    MQTT_PASSWORD,
)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("test/poop")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


def setup_mqtt_client():
    print(MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASSWORD)
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    if MQTT_USER is not None:
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    return client


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# client.loop_forever()M


def build_random_color(range=255):
    return (
        random.randint(0, range),
        random.randint(0, range),
        random.randint(0, range),
    )


def build_pygame_screen():
    pygame.display.set_caption("RGB MATRIX")
    return pygame.display.set_mode((LED_COLS, LED_ROWS), SCALED | RESIZABLE, 32)


def render_pygame(screen, matrix=None):
    if matrix is not None:
        flipped = pygame.transform.flip(screen, True, False)
        new_screen = pygame.Surface(
            (flipped.get_rect().width, flipped.get_rect().height)
        )

        new_screen.blit(flipped, (0, 0), special_flags=BLEND_RGBA_ADD)
        imgdata = pygame.surfarray.array3d(new_screen)
        print(imgdata)

        image_rgb = Image.fromarray(imgdata, mode="RGB")
        matrix.SetImage(image_rgb)
    pygame.display.flip()
