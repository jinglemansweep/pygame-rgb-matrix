from pygameft import FTClient

from wideboy.config import (
    FT_HOST,
    FT_PORT,
    FT_WIDTH,
    FT_HEIGHT,
    FT_LAYER,
    FT_TRANSPARENT,
    FT_TILE_WIDTH,
    FT_TILE_HEIGHT,
)


def connect_flaschen_taschen():
    return FTClient(
        FT_HOST,
        FT_PORT,
        width=FT_WIDTH,
        height=FT_HEIGHT,
        layer=FT_LAYER,
        transparent=FT_TRANSPARENT,
        tile_width=FT_TILE_WIDTH,
        tile_height=FT_TILE_HEIGHT,
    )
