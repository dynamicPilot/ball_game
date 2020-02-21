"""
Gate Class (based on Gameobject).
---
Класс для ворот (на основе GameOdject).
"""

import pygame
from game_object import GameObject

class Gate(GameObject):
    def __init__(self, x, y, width, height, color, player):
        GameObject.__init__(self, x, y, width, height)
        self.color = color
        self.player = player

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
