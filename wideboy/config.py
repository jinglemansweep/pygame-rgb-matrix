import os

# Read environment variable configuration and set any default values

DEBUG = os.environ.get("DEBUG", "false") == "true"
PROFILING = os.environ.get("PROFILING", "")
GUI_ENABLED = os.environ.get("GUI_ENABLED", "false").lower() == "true"

PYGAME_FPS = int(os.environ.get("PYGAME_FPS", 60))
PYGAME_BITS_PER_PIXEL = int(os.environ.get("PYGAME_BITS_PER_PIXEL", 16))

LED_ROWS = int(os.environ.get("LED_ROWS", 64))  # 64
LED_COLS = int(os.environ.get("LED_COLS", 64))  # 64
LED_CHAIN = int(os.environ.get("LED_CHAIN", 1))  # 8
LED_PARALLEL = int(os.environ.get("LED_PARALLEL", 1))  # 3
PANEL_ROWS = int(os.environ.get("PANEL_ROWS", 1))
PANEL_COLS = int(os.environ.get("PANEL_COLS", 1))

FT_HOST = os.environ.get("FT_HOST", "localhost")
FT_PORT = int(os.environ.get("FT_PORT", 1337))
FT_LAYER = int(os.environ.get("FT_LAYER", 5))
FT_TRANSPARENT = os.environ.get("FT_TRANSPARENT", "true").lower() == "true"

RSS_URL = os.environ.get("RSS_URL")
RSS_UPDATE_INTERVAL = int(os.environ.get("RSS_UPDATE_INTERVAL", 3600))  # 1 hour

MQTT_HOST = os.environ.get("MQTT_HOST")
MQTT_PORT = int(os.environ.get("MQTT_PORT", 8883))
MQTT_USER = os.environ.get("MQTT_USER")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD")

DEVICE_NAME = os.environ.get("DEVICE_NAME", "default")

IMAGE_PATH = "images"
TICKER_DISPLAY_INTERVAL = int(os.environ.get("TICKER_DISPLAY_INTERVAL", 300))  # 5 mins
