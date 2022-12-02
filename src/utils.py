import pygame
import random
from PIL import Image

def build_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def render_pygame_to_matrix(screen, matrix):
    pygame.display.flip()
    #time.sleep(0.01)
    screen.blit(pygame.transform.flip(screen, False, True), dest=(0, 0))
    imgdata = pygame.surfarray.array3d(screen)    
    image_rgb = Image.fromarray(imgdata, mode="RGB")
    matrix.SetImage(image_rgb)