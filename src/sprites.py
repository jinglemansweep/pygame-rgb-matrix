import pygame

COLOR_SURFACE = (0, 0, 0)


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, w, h, color):
        super().__init__()
        self.image = pygame.Surface([w, h])
        self.image.fill(COLOR_SURFACE)
        self.image.set_colorkey(COLOR_SURFACE)
        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, w, h))
        self.rect = self.image.get_rect()
