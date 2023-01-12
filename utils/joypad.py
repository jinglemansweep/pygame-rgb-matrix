import os
import sys
import time
import pygame
from pygame.locals import *

os.putenv("SDL_VIDEODRIVER", "dummy")

pygame.init()  # Initializes Pygame


class JoyPad:
    def __init__(self, device_index):
        pygame.joystick.init()
        self.joypad = pygame.joystick.Joystick(device_index)
        self.joypad.init()
        self.pad = None
        self.action = None

    def process_event(self, event):
        if event.type == pygame.JOYBUTTONDOWN:
            self.action = event.dict["button"]
        if event.type == pygame.JOYHATMOTION:
            self.pad = event.dict["value"]
        return self.pad, self.action


joypad = JoyPad(0)

p1_pad = None
p1_action = None

while True:
    for event in pygame.event.get():
        p1_pad, p1_action = joypad.process_event(event)
    print(p1_pad, p1_action)

"""
from evdev import InputDevice, categorize, ecodes, KeyEvent

gamepad = InputDevice("/dev/input/event0")
last = {"ABS_RZ": 128, "ABS_Z": 128}
for event in gamepad.read_loop():
    print(event.type)
    if event.type == ecodes.EV_ABS:
        print(event)
        absevent = categorize(event)
        #'print(absevent)
"""
