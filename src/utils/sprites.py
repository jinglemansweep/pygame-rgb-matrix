import pygame


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, position=None):
        super().__init__()
        if position is not None:
            self.rect[0], self.rect[1] = position


class TilesetSprite(BaseSprite):
    def __init__(self, tileset, tile_index, position):
        self.tileset = tileset
        self.image = self.tileset.tiles[tile_index]
        self.rect = self.image.get_rect()
        super().__init__(position)

    def get_viewport_position(self, camera):
        return (self.rect[0] - camera.position[0], self.rect[1] - camera.position[1])
