import pygame
import random
from PIL import Image


def build_random_color(range=255):
    return (
        random.randint(0, range),
        random.randint(0, range),
        random.randint(0, range),
    )


def render_pygame(screen, matrix=None):
    if matrix is not None:
        screen.blit(pygame.transform.flip(screen, False, True), dest=(0, 0))
        imgdata = pygame.surfarray.array3d(screen)
        image_rgb = Image.fromarray(imgdata, mode="RGB")
        matrix.SetImage(image_rgb)
    pygame.display.flip()
