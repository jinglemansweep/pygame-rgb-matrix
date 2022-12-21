import pygame
import random
from pygame.locals import *


class Camera:
    def __init__(
        self,
        position=[0, 0],
        direction=[0, 0],
        speed=[0, 0],
        accelleration=[0, 0],
        friction=0.999,
    ):
        self.position = [0, 0]
        self.direction = list(direction)
        self.speed = list(speed)
        self.acceleration = list(accelleration)
        self.friction = friction
        self.target_position = [None, None]

    def __str__(self):
        return f"<Camera pos={self.position} dir={self.direction} speed={self.speed} accel={self.acceleration}>"

    def set_target_position(self, position):
        print(f"camera->set_target_position: position={position}")
        for axis in [0, 1]:
            if position[axis] is not None:
                self.target_position[axis] = position[axis]

    def update(self):
        self._set_motion_props()
        for axis in [0, 1]:
            self.position[axis] += self.direction[axis] * self.speed[axis]

    def _set_motion_props(self):
        # iterate through x and y axis
        for axis in [0, 1]:
            # if speed is less than maximum, apply acceleration
            if self.speed[axis] < 1:
                self.speed[axis] += self.acceleration[axis]
            # if we are moving to a target, calculate distance and stop accelerating within 100 pixels of target
            if self.target_position[axis] is not None:
                distance = abs((self.target_position[axis] or 0) - self.position[axis])
                if distance < 100:
                    self.acceleration[axis] = 0
            # decrease speed gradually by applying friction
            self.speed[axis] *= self.friction
            # apply directions based on target
            if self.target_position[axis] is not None:
                if int(self.target_position[axis]) != int(self.position[axis]):
                    self.direction[axis] = (
                        1 if self.target_position[axis] > self.position[axis] else -1
                    )
                else:
                    self.direction[axis] = 0
                    self.target_position[axis] = None
                    self.position[axis] = float(round(self.position[axis]))


class Projection:
    def __init__(self, rect, camera_position=(0, 0)):
        self.rect = rect
        self.camera = Camera(position=camera_position)

    def update(self):
        self.camera.update()

    def blit(self, surface, position, screen):
        temp_surface = pygame.Surface((self.rect[2], self.rect[3]), SRCALPHA)
        temp_surface.blit(
            surface,
            (
                position[0] - self.camera.position[0],
                position[1] - self.camera.position[1],
            ),
        )
        screen.blit(temp_surface, self.rect, (0, 0, self.rect[2], self.rect[3]))

    def __str__(self):
        return f"<Projection rect={self.rect} camera={self.camera}>"
