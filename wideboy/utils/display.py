from pygameft import FTClient

from wideboy.config import (
    LED_CHAIN,
    LED_PARALLEL,
    LED_ROWS,
    LED_COLS,
    FT_HOST,
    FT_PORT,
    FT_LAYER,
    FT_TRANSPARENT,
)


def connect_flaschen_taschen():
    return FTClient(
        FT_HOST,
        FT_PORT,
        width=LED_COLS * LED_CHAIN,
        height=LED_ROWS * LED_PARALLEL,
        layer=FT_LAYER,
        transparent=FT_TRANSPARENT,
        tile_width=LED_COLS * 2,
        tile_height=LED_ROWS,
    )
