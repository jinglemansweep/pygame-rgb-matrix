import argparse
import os
import pygame
import random
import sys
import time

from PIL import Image
from PIL import ImageDraw
from pygame.locals import QUIT

sys.path.append(
    os.path.abspath(
        os.path.dirname(__file__) + "/../lib/rpi-rgb-led-matrix/bindings/python"
    )
)
from rgbmatrix import RGBMatrix, RGBMatrixOptions

parser = argparse.ArgumentParser()

parser.add_argument(
    "-r",
    "--led-rows",
    action="store",
    help="Display rows. 16 for 16x32, 32 for 32x32. Default: 32",
    default=32,
    type=int,
)
parser.add_argument(
    "--led-cols",
    action="store",
    help="Panel columns. Typically 32 or 64. (Default: 32)",
    default=32,
    type=int,
)
parser.add_argument(
    "-c",
    "--led-chain",
    action="store",
    help="Daisy-chained boards. Default: 1.",
    default=1,
    type=int,
)
parser.add_argument(
    "-P",
    "--led-parallel",
    action="store",
    help="For Plus-models or RPi2: parallel chains. 1..3. Default: 1",
    default=1,
    type=int,
)
parser.add_argument(
    "-p",
    "--led-pwm-bits",
    action="store",
    help="Bits used for PWM. Something between 1..11. Default: 11",
    default=11,
    type=int,
)
parser.add_argument(
    "-b",
    "--led-brightness",
    action="store",
    help="Sets brightness level. Default: 100. Range: 1..100",
    default=100,
    type=int,
)
parser.add_argument(
    "-m",
    "--led-gpio-mapping",
    help="Hardware Mapping: regular, adafruit-hat, adafruit-hat-pwm",
    choices=["regular", "regular-pi1", "adafruit-hat", "adafruit-hat-pwm"],
    type=str,
)
parser.add_argument(
    "--led-scan-mode",
    action="store",
    help="Progressive or interlaced scan. 0 Progressive, 1 Interlaced (default)",
    default=1,
    choices=range(2),
    type=int,
)
parser.add_argument(
    "--led-pwm-lsb-nanoseconds",
    action="store",
    help="Base time-unit for the on-time in the lowest significant bit in nanoseconds. Default: 130",
    default=130,
    type=int,
)
parser.add_argument(
    "--led-show-refresh",
    action="store_true",
    help="Shows the current refresh rate of the LED panel",
)
parser.add_argument(
    "--led-slowdown-gpio",
    action="store",
    help="Slow down writing to GPIO. Range: 0..4. Default: 1",
    default=1,
    type=int,
)
parser.add_argument(
    "--led-no-hardware-pulse",
    action="store",
    help="Don't use hardware pin-pulse generation",
)
parser.add_argument(
    "--led-rgb-sequence",
    action="store",
    help="Switch if your matrix has led colors swapped. Default: RGB",
    default="RGB",
    type=str,
)
parser.add_argument(
    "--led-pixel-mapper",
    action="store",
    help='Apply pixel mappers. e.g "Rotate:90"',
    default="",
    type=str,
)
parser.add_argument(
    "--led-row-addr-type",
    action="store",
    help="0 = default; 1=AB-addressed panels; 2=row direct; 3=ABC-addressed panels; 4 = ABC Shift + DE direct",
    default=0,
    type=int,
    choices=[0, 1, 2, 3, 4],
)
parser.add_argument(
    "--led-multiplexing",
    action="store",
    help="Multiplexing type: 0=direct; 1=strip; 2=checker; 3=spiral; 4=ZStripe; 5=ZnMirrorZStripe; 6=coreman; 7=Kaler2Scan; 8=ZStripeUneven... (Default: 0)",
    default=0,
    type=int,
)
parser.add_argument(
    "--led-panel-type",
    action="store",
    help="Needed to initialize special panels. Supported: 'FM6126A'",
    default="",
    type=str,
)
parser.add_argument(
    "--led-no-drop-privs",
    dest="drop_privileges",
    help="Don't drop privileges from 'root' after initializing the hardware.",
    action="store_false",
)
parser.set_defaults(drop_privileges=True)

args = parser.parse_args()
options = RGBMatrixOptions()
if args.led_gpio_mapping != None:
    options.hardware_mapping = args.led_gpio_mapping
options.rows = args.led_rows
options.cols = args.led_cols
options.chain_length = args.led_chain
options.parallel = args.led_parallel
options.row_address_type = args.led_row_addr_type
options.multiplexing = args.led_multiplexing
options.pwm_bits = args.led_pwm_bits
options.brightness = args.led_brightness
options.pwm_lsb_nanoseconds = args.led_pwm_lsb_nanoseconds
options.led_rgb_sequence = args.led_rgb_sequence
options.pixel_mapper_config = args.led_pixel_mapper
options.panel_type = args.led_panel_type

if args.led_show_refresh:
    options.show_refresh_rate = 1

if args.led_slowdown_gpio != None:
    options.gpio_slowdown = args.led_slowdown_gpio
if args.led_no_hardware_pulse:
    options.disable_hardware_pulsing = True
if not args.drop_privileges:
    options.drop_privileges = False

COLOR = (255, 255, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_BACKGROUND = (0, 0, 0)
WIDTH = 64
HEIGHT = 64

matrix = RGBMatrix(options=options)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, w, h, color):
        super().__init__()
        self.image = pygame.Surface([w, h])
        self.image.fill(COLOR_BACKGROUND)
        self.image.set_colorkey(COLOR_BACKGROUND)
        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, w, h))
        self.rect = self.image.get_rect()


def build_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


os.putenv("SDL_VIDEODRIVER", "dummy")
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Hello World!")

x = 0
y = 0

clock = pygame.time.Clock()

actors = pygame.sprite.Group()
for i in range(3, random.randint(3, 50)):
    s = Sprite(random.randint(1, 3), random.randint(1, 3), build_random_color())
    s.rect.x = random.randint(0, 63)
    s.rect.y = random.randint(0, 63)
    actors.add(s)


while True:  # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    for actor in actors:
        print(actor.rect)
        actor.rect.x += 1
        if actor.rect.x > WIDTH:
            actor.rect.y += 1
            actor.rect.x = 0
        if actor.rect.y > HEIGHT:
            actor.rect.y = 0
        actor.update()
    actors.update()
    screen.fill(COLOR_BACKGROUND)
    actors.draw(screen)
    pygame.display.flip()
    time.sleep(0.01)
    screen.blit(pygame.transform.flip(screen, False, True), dest=(0, 0))
    imgdata = pygame.surfarray.array3d(screen)    
    image_rgb = Image.fromarray(imgdata, mode="RGB")
    matrix.SetImage(image_rgb)
    clock.tick(200)
