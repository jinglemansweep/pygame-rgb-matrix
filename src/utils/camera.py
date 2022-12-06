import random


class Camera:
    def __init__(
        self,
        map_size,
        viewport_size,
        tile_size,
        positions=[[0, 0]],
        direction=[0, 0],
        speed=[0, 0],
        accelleration=[0, 0],
        friction=0.999,
    ):

        self.map_size = map_size
        self.viewport_size = viewport_size
        self.tile_size = tile_size
        self.positions = list(positions)
        self.position_idx = 0
        self.position = self.positions[self.position_idx]
        self.direction = list(direction)
        self.speed = list(speed)
        self.acceleration = list(accelleration)
        self.friction = friction
        self.target_position = [None, None]

    def set_target_position(self, position):
        for axis in [0, 1]:
            if position[axis] is not None:
                self.target_position[axis] = position[axis]

    def move_next_position(self):
        self.position_idx += 1
        if self.position_idx > len(self.positions) - 1:
            self.position_idx = 0
        self.set_target_position(self.positions[self.position_idx])
        self.acceleration = [0.5, 0.5]

    def set_random_position(self, bounds=None):
        if bounds is None:
            bounds = [None, None]
        bound_x = (
            bounds[0]
            if bounds[0] is not None
            else (self.map_size[0] - self.viewport_size[0]) * self.tile_size[0]
        )
        bound_y = (
            bounds[1]
            if bounds[1] is not None
            else (self.map_size[1] - self.viewport_size[1]) * self.tile_size[1]
        )
        position = (
            random.randint(0, bound_x),
            random.randint(0, bound_y),
        )
        self.set_target_position(position)
        self.acceleration = [0.5, 0.5]

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
