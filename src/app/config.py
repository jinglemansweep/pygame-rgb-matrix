import os

# Read environment variable configuration and set any default values

DEBUG = os.environ.get("DEBUG", "false") == "true"
PROFILING = os.environ.get("PROFILING", "")
GUI_ENABLED = os.environ.get("GUI_ENABLED", "false").lower() == "true"

PYGAME_FPS = int(os.environ.get("PYGAME_FPS", 60))
PYGAME_BITS_PER_PIXEL = int(os.environ.get("PYGAME_BITS_PER_PIXEL", 16))

LED_ENABLED = os.environ.get("LED_ENABLED", "true").lower() == "true"
LED_GPIO_MAPPING = os.environ.get("LED_GPIO_MAPPING")  # regular, adafruit, adafruit-pwm
LED_ROWS = int(os.environ.get("LED_ROWS", 64))  # 64
LED_COLS = int(os.environ.get("LED_COLS", 64))  # 64
LED_CHAIN = int(os.environ.get("LED_CHAIN", 1))  # 8
LED_PARALLEL = int(os.environ.get("LED_PARALLEL", 1))  # 3
LED_MULTIPLEXING = int(os.environ.get("LED_MULTIPLEXING", 0))  # 0-18
LED_PIXEL_MAPPER = os.environ.get("LED_PIXEL_MAPPER", "")  # U-mapper;V-mapper;Rotate:90
LED_PWM_BITS = int(os.environ.get("LED_PWM_BITS", 11))  # 1-11
LED_BRIGHTNESS = int(os.environ.get("LED_BRIGHTNESS", 100))  # 0-100
LED_SCAN_MODE = int(os.environ.get("LED_SCAN_MODE", 0))  # 0,1
LED_ROW_ADDR_TYPE = int(os.environ.get("LED_ROW_ADDR_TYPE", 0))  # 0-4
LED_SHOW_REFRESH = (
    os.environ.get("LED_SHOW_REFRESH", "false").lower() == "true"
)  # true/false
LED_LIMIT_REFRESH = int(os.environ.get("LED_LIMIT_REFRESH", 0))  # 0
LED_INVERSE = os.environ.get("LED_INVERSE", "false").lower() == "true"  # true/false
LED_RGB_SEQUENCE = os.environ.get("LED_RGB_SEQUENCE", "RGB")  # RGB, RBG
LED_PWM_LSB_NANOSECONDS = int(os.environ.get("LED_PWM_LSB_NANOSECONDS", 130))  # 130
LED_PWM_DITHER_BITS = int(os.environ.get("LED_PWM_DITHER_BITS", 0))  # 0-2
LED_NO_HARDWARE_PULSE = (
    os.environ.get("LED_NO_HARDWARE_PULSE", "false").lower() == "true"
)  # true/false
LED_PANEL_TYPE = os.environ.get("LED_PANEL_TYPE")  # FM6126A, FM6127
LED_SLOWDOWN_GPIO = int(os.environ.get("LED_SLOWDOWN_GPIO", 0))  # 0-4
LED_DAEMON = os.environ.get("LED_DAEMON", "false").lower() == "true"  # true/false
LED_NO_DROP_PRIVS = (
    os.environ.get("LED_NO_DROP_PRIVS", "false").lower() == "true"
)  # true/false

PANEL_ROWS = int(os.environ.get("PANEL_ROWS", 1))
PANEL_COLS = int(os.environ.get("PANEL_COLS", 1))

RSS_URL = os.environ.get("RSS_URL")
RSS_UPDATE_INTERVAL = int(os.environ.get("RSS_UPDATE_INTERVAL", 3600))  # 1 hour

MQTT_HOST = os.environ.get("MQTT_HOST")
MQTT_PORT = int(os.environ.get("MQTT_PORT", 8883))
MQTT_USER = os.environ.get("MQTT_USER")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD")

DEVICE_NAME = os.environ.get("DEVICE_NAME", "default")

IMAGE_PATH = "images/photos"
TICKER_DISPLAY_INTERVAL = int(os.environ.get("TICKER_DISPLAY_INTERVAL", 300))  # 5 mins

# Construct RGB Matrix options object
matrix_options = None

if LED_ENABLED:
    from rgbmatrix import RGBMatrixOptions

    matrix_options = RGBMatrixOptions()
    if LED_ROWS:
        matrix_options.rows = LED_ROWS
    if LED_COLS:
        matrix_options.cols = LED_COLS
    if LED_CHAIN:
        matrix_options.chain_length = LED_CHAIN
    if LED_PARALLEL:
        matrix_options.parallel = LED_PARALLEL
    if LED_ROW_ADDR_TYPE:
        matrix_options.row_address_type = LED_ROW_ADDR_TYPE
    if LED_MULTIPLEXING:
        matrix_options.multiplexing = LED_MULTIPLEXING
    if LED_PIXEL_MAPPER:
        matrix_options.pixel_mapper_config = LED_PIXEL_MAPPER
    if LED_PWM_BITS:
        matrix_options.pwm_bits = LED_PWM_BITS
    if LED_BRIGHTNESS:
        matrix_options.brightness = LED_BRIGHTNESS
    if LED_SCAN_MODE:
        matrix_options.scan_mode = LED_SCAN_MODE
    if LED_ROW_ADDR_TYPE:
        matrix_options.row_addr_type = LED_ROW_ADDR_TYPE
    if LED_SHOW_REFRESH:
        matrix_options.show_refresh_rate = LED_SHOW_REFRESH
    if LED_LIMIT_REFRESH:
        matrix_options.limit_refresh_rate_hz = LED_LIMIT_REFRESH
    if LED_INVERSE:
        matrix_options.inverse = LED_INVERSE
    if LED_RGB_SEQUENCE:
        matrix_options.led_rgb_sequence = LED_RGB_SEQUENCE
    if LED_PWM_LSB_NANOSECONDS:
        matrix_options.pwm_lsb_nanoseconds = LED_PWM_LSB_NANOSECONDS
    if LED_PWM_DITHER_BITS:
        matrix_options.pwm_dither_bits = LED_PWM_DITHER_BITS
    if LED_NO_HARDWARE_PULSE:
        matrix_options.disable_hardware_pulsing = 1
    if LED_PANEL_TYPE:
        matrix_options.panel_type = LED_PANEL_TYPE
    if LED_SLOWDOWN_GPIO:
        matrix_options.gpio_slowdown = LED_SLOWDOWN_GPIO
    if LED_DAEMON:
        matrix_options.daemon = LED_DAEMON
    if LED_NO_DROP_PRIVS:
        matrix_options.drop_privileges = 1
