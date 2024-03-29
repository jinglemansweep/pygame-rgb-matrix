from pygameft import FTClient  # type: ignore

from wideboy.config import (
    DEBUG,
    FT_HOST,
    FT_PORT,
    FT_POS,
    FT_SIZE,
    FT_LAYER,
    FT_TRANSPARENT,
    FT_TILE_SIZE,
)


def connect_flaschen_taschen() -> FTClient:
    return FTClient(
        FT_HOST,
        FT_PORT,
        FT_POS,
        FT_SIZE,
        layer=FT_LAYER,
        transparent=FT_TRANSPARENT,
        tile_size=FT_TILE_SIZE,
        debug=DEBUG,
    )
