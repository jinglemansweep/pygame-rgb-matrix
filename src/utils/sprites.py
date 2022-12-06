import pygame
import random

ACTION_STILL = 0
ACTION_WALKING = 1


class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, position=None):
        super().__init__()
        if position is not None:
            self.rect[0], self.rect[1] = position
        self._timers = {}

    def update(self, *args, **kwargs):
        self._timers_update()

    def _timers_update(self):
        for k, v in self._timers.items():
            if self._timers[k] > 0:
                self._timers[k] = self._timers[k] - 1


class TilesetSprite(BaseSprite):
    def __init__(self, tileset, tile_index, position):
        self.tileset = tileset
        self.tile_index = tile_index
        self.image = self.tileset.tiles[self.tile_index]
        self.rect = self.image.get_rect()
        super().__init__(position)

    def get_viewport_position(self, camera):
        return (self.rect[0] - camera.position[0], self.rect[1] - camera.position[1])


class AnimationMixin:
    def __init__(
        self,
        direction=[0, 0],
        speed=[0, 0],
        bounds=[None, None],
        sprite_frames=0,
        animate_every_x_frame=2,
        move_every_x_frame=2,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.image_orig = self.image.copy()
        if direction is None:
            direction = [0, 0]
        if speed is None:
            speed = [0, 0]
        if bounds is None:
            bounds = [None, None]
        self.direction = list(direction)
        self.direction_last = [1, 1]
        self.speed = list(speed)
        self.bounds = list(bounds)
        self.target_position = [None, None]
        self.sprite_frames = sprite_frames
        self.sprite_frame_index = 0
        self.animate_every_x_frame = animate_every_x_frame
        self.move_every_x_frame = move_every_x_frame
        self.image_orig = self.image.copy()
        self.action = ACTION_STILL
        self.timers = dict(collision=0)
        self._random_generate_seed()

    def update(self, frame, **kwargs):
        if frame % self.move_every_x_frame == 0:
            # calculate sprite movement and apply
            self._set_motion_props()
            for axis in [0, 1]:
                self.rect[axis] += self.direction[axis] * self.speed[axis]
        # random reseed
        self._random_generate_seed()

    def set_target_position(self, position):
        # print(f"BaseSprite->set_target_position: position={position}")
        for axis in [0, 1]:
            if position[axis] is not None:
                self.target_position[axis] = position[axis]

    def stop(self):
        for axis in [0, 1]:
            self.direction[axis] = 0
            self.target_position[axis] = None
            self.rect[axis] = float(round(self.rect[axis]))
            self.action = ACTION_STILL

    def _set_motion_props(self):
        # iterate through x and y axis
        for axis in [0, 1]:
            # apply directions based on target
            if self.target_position[axis] is not None:
                if int(self.target_position[axis]) != int(self.rect[axis]):
                    dir = 1 if self.target_position[axis] > self.rect[axis] else -1
                    self.direction[axis] = dir
                    self.direction_last[axis] = dir
                    self.action = ACTION_WALKING
                else:
                    self.stop()

    def _random_generate_seed(self):
        self._random_seed = random.randint(0, 9999)


class CollisionMixin:
    def __init__(self, collidables=None, **kwargs):
        super().__init__(**kwargs)
        if collidables is None:
            collidables = []
        self._collision_collidables = collidables
        self._timers["collision"] = 0

    def _collision_detect(self):
        if self._timers["collision"] > 0:
            return False
        collisions = [self.rect.colliderect(c) for c in self._collision_collidables]
        has_collided = any(collisions)
        if has_collided:
            self._timers["collision"] = 1000
            # print("collision")
        return has_collided
