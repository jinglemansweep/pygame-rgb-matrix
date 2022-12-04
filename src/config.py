import os

# Read environment variable configuration and set any default values
GUI_ENABLED = os.environ.get("GUI_ENABLED", "false").lower() == "true"
LED_ENABLED = os.environ.get("LED_ENABLED", "true").lower() == "true"
LED_ROWS = int(os.environ.get("LED_ROWS", 64))
LED_COLS = int(os.environ.get("LED_COLS", 64))
LED_CHAIN = int(os.environ.get("LED_CHAIN", 1))
LED_PARALLEL = int(os.environ.get("LED_PARALLEL", 1))
LED_PWM_BITS = int(os.environ.get("LED_PWM_BITS", 11))
LED_BRIGHTNESS = int(os.environ.get("LED_BRIGHTNESS", 100))
LED_GPIO_MAPPING = os.environ.get("LED_GPIO_MAPPING", None)
LED_SCAN_MODE = int(os.environ.get("LED_SCAN_MODE", 1))
LED_PWM_LSB_NANOSECONDS = int(os.environ.get("LED_PWM_LSB_NANOSECONDS", 130))
LED_SHOW_REFRESH = os.environ.get("LED_SHOW_REFRESH", False)
LED_SLOWDOWN_GPIO = int(os.environ.get("LED_SLOWDOWN_GPIO", 1))
LED_NO_HARDWARE_PULSE = os.environ.get("LED_NO_HARDWARE_PULSE", False)
LED_RGB_SEQUENCE = os.environ.get("LED_RGB_SEQUENCE", "RGB")
LED_PIXEL_MAPPER = os.environ.get("LED_PIXEL_MAPPER", "")
LED_ROW_ADDR_TYPE = int(os.environ.get("LED_ROW_ADDR_TYPE", 0))
LED_MULTIPLEXING = int(os.environ.get("LED_MULTIPLEXING", 0))
LED_PANEL_TYPE = os.environ.get("LED_PANEL_TYPE", "")
MQTT_HOST = os.environ.get("MQTT_HOST", "localhost")
MQTT_PORT = int(os.environ.get("MQTT_PORT", "1883"))
MQTT_USER = os.environ.get("MQTT_USER", None)
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD", "")

# Construct RGB Matrix options object
matrix_options = None

if LED_ENABLED:
    from rgbmatrix import RGBMatrixOptions

    matrix_options = RGBMatrixOptions()
    if LED_GPIO_MAPPING is not None:
        matrix_options.hardware_mapping = LED_GPIO_MAPPING
    matrix_options.rows = LED_ROWS
    matrix_options.cols = LED_COLS
    matrix_options.chain_length = LED_CHAIN
    matrix_options.parallel = LED_PARALLEL
    matrix_options.row_address_type = LED_ROW_ADDR_TYPE
    matrix_options.multiplexing = LED_MULTIPLEXING
    matrix_options.pwm_bits = LED_PWM_BITS
    matrix_options.brightness = LED_BRIGHTNESS
    matrix_options.pwm_lsb_nanoseconds = LED_PWM_LSB_NANOSECONDS
    matrix_options.led_rgb_sequence = LED_RGB_SEQUENCE
    matrix_options.pixel_mapper_config = LED_PIXEL_MAPPER
    matrix_options.panel_type = LED_PANEL_TYPE
    matrix_options.show_refresh_rate = 1 if LED_SHOW_REFRESH else 0
    if LED_SLOWDOWN_GPIO is not None:
        matrix_options.gpio_slowdown = LED_SLOWDOWN_GPIO
    if LED_NO_HARDWARE_PULSE:
        matrix_options.disable_hardware_pulsing = True
    matrix_options.drop_privileges = True

if not GUI_ENABLED:
    pass
    os.putenv("SDL_VIDEODRIVER", "dummy")
