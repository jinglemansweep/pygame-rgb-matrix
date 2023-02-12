from pygameft import FTClient

from wideboy.config import (
    FT_HOST,
    FT_PORT,
    FT_POS,
    FT_SIZE,
    FT_LAYER,
    FT_TRANSPARENT,
    FT_TILE_SIZE,
)


def connect_flaschen_taschen():
    return FTClient(
        FT_HOST,
        FT_PORT,
        FT_POS,
        FT_SIZE,
        layer=FT_LAYER,
        transparent=FT_TRANSPARENT,
        tile_size=FT_TILE_SIZE,
    )
