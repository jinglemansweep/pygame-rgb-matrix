import os

# Read environment variable configuration and set any default values

DEBUG = os.environ.get("DEBUG", "false") == "true"
PROFILING = os.environ.get("PROFILING", "")
PYGAME_FPS = int(os.environ.get("PYGAME_FPS", 60))

FT_HOST = os.environ.get("FT_HOST", "localhost")
FT_PORT = int(os.environ.get("FT_PORT", 1337))
FT_WIDTH = int(os.environ.get("FT_WIDTH", 256))
FT_HEIGHT = int(os.environ.get("FT_HEIGHT", 192))
FT_SIZE = (FT_WIDTH, FT_HEIGHT)
FT_POS_X = int(os.environ.get("FT_POS_X", 0))
FT_POS_Y = int(os.environ.get("FT_POS_Y", 0))
FT_POS = (FT_POS_X, FT_POS_Y)
FT_LAYER = int(os.environ.get("FT_LAYER", 5))
FT_TRANSPARENT = os.environ.get("FT_TRANSPARENT", "true").lower() == "true"
FT_TILE_WIDTH = int(os.environ.get("FT_TILE_WIDTH", 64))
FT_TILE_HEIGHT = int(os.environ.get("FT_TILE_HEIGHT", 64))
FT_TILE_SIZE = (FT_TILE_WIDTH, FT_TILE_HEIGHT)

MQTT_HOST = os.environ.get("MQTT_HOST")
MQTT_PORT = int(os.environ.get("MQTT_PORT", 8883))
MQTT_USER = os.environ.get("MQTT_USER")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD")

DEVICE_NAME = os.environ.get("DEVICE_NAME", "default")

IMAGE_PATH = "images"
TICKER_DISPLAY_INTERVAL = int(os.environ.get("TICKER_DISPLAY_INTERVAL", 300))  # 5 mins
