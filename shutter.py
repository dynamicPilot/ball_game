"""
Shutters Classes: left and right (based on Gameobject).
"""

import pygame

import config as c
from game_object import GameObject

class Shutter_right(GameObject):
    def __init__(self, x, y, w, h, color, offset):
        GameObject.__init__(self, x, y, w, h)
        self.color = color
        self.offset = offset
        self.moving_up = False
        self.moving_down = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def update(self):
        if self.moving_up:
            dy = -(min(self.offset, self.top-c.up_margin))
        elif self.moving_down:
            dy = min(self.offset, c.screen_height - c.margin - self.bottom)
        else:
            return

        self.move(0, dy)

    def handle(self, key):
        if key == pygame.K_UP:
            self.moving_up = not self.moving_up
        if key == pygame.K_DOWN:
            self.moving_down = not self.moving_down


class Shutter_left(GameObject):
    def __init__(self, x, y, w, h, color, offset):
        GameObject.__init__(self, x, y, w, h)
        self.color = color
        self.offset = offset
        self.moving_up = False
        self.moving_down = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def update(self):
        if self.moving_up:
            dy = -(min(self.offset, self.top-c.up_margin))
        elif self.moving_down:
            dy = min(self.offset, c.screen_height - c.margin - self.bottom)
        else:
            return

        self.move(0, dy)

    def handle(self, key):
        if key == pygame.K_w:
            self.moving_up = not self.moving_up
        if key == pygame.K_s:
            self.moving_down = not self.moving_down



