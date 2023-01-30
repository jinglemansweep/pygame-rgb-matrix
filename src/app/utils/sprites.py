import pygame
import logging

logger = logging.getLogger("sprites")


class StageSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frame = 0
        self.mode = "idle"  # idle, hiding, showing
        self.mode_change_frame_start = 0

    def update(self, frame):
        self.frame = frame

    def set_mode(self, mode):
        # logger.info(f"Mode: mode={mode} start={self.frame}")
        self.mode = mode
        self.mode_change_frame_start = self.frame
