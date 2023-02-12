from pygameft import FTClient

from wideboy.config import (
    LED_ROWS,
    LED_COLS,
    FT_HOST,
    FT_PORT,
    FT_LAYER,
    FT_TRANSPARENT,
)


def connect_flaschen_taschen(display_size):
    return FTClient(
        FT_HOST,
        FT_PORT,
        width=display_size[0],
        height=display_size[1],
        layer=FT_LAYER,
        transparent=FT_TRANSPARENT,
        tile_width=LED_COLS * 2,
        tile_height=LED_ROWS,
    )
