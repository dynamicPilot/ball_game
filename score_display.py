"""
ScoreDisplay Class (based on Gameobject).
---
Класс для дисплеев, отображающих очки игроков (на основе GameOdject).
"""

import pygame

import config as c
import colors
from game_object import GameObject
from text_object import TextObject

class ScoreDisplay(GameObject):
    def __init__ (self, x, y):
        GameObject.__init__(self, x, y, c.score_display_w, c.score_display_h)
        self.color = c.score_display_color
      
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def update(self):
        super().update()





    