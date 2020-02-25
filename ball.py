"""
Ball Class (based on Gameobject).
"""

import pygame

from game_object import GameObject

class Ball(GameObject):
    def __init__(self, x_center, y_center, r, color, speed, special_effect=None):
        GameObject.__init__(self, x_center - r, y_center - r, r * 2, r * 2, speed)
        self.radius = r
        self.diameter = r * 2
        self.color = color
        self.special_effect = special_effect

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.center, self.radius)

    def update(self):
        super().update()
