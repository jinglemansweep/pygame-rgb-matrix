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
        # screen = pygame.Surface((flipped.get_rect().width, flipped.get_rect().height))
        screen.blit(
            flipped,
            (0, 0),
        )
        imgdata = pygame.surfarray.array3d(screen)
        image_rgb = Image.fromarray(imgdata, mode="RGB")
        matrix.SetImage(image_rgb)
    pygame.display.flip()


class Camera:
    def __init__(
        self,
        map_size,
        viewport_size,
        tile_size,
        position=None,
        direction=None,
        speed=None,
    ):
        if position is None:
            position = [0, 0]
        if direction is None:
            direction = [0, 0]
        if speed is None:
            speed = [0, 0]
        self.map_size = map_size
        self.viewport_size = viewport_size
        self.tile_size = tile_size
        self.position = list(position)
        self.direction = list(direction)
        self.speed = list(speed)

    def get_position(self):
        return (self.position[0], self.position[1])

    def update(self):
        for axis in [0, 1]:
            self.position[axis] += self.direction[axis] * self.speed[axis]
            if (
                self.position[axis]
                > (self.map_size[axis] - self.viewport_size[axis]) * self.tile_size
            ):
                self.direction[axis] = -1
            if self.position[axis] < 0:
                self.direction[axis] = 1
