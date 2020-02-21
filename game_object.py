"""
Base GameObject Class for creating a game object.
---
Базовый класс для создания игровых объектов.
"""

import pygame

class GameObject:
    def __init__(self, x, y, w, h, speed=(0,0)):
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = speed

    @property
    def left(self):
        """
        Return left-x coordinate of Rect object 
        """
        return self.rect.left

    @property
    def right(self):
        """
        Return right-x coordinate of Rect object 
        """
        return self.rect.right

    @property
    def top(self):
        """
        Return top-y coordinate of Rect object 
        """
        return self.rect.top

    @property
    def bottom(self):
        """
        Return bottom-y coordinate of Rect object 
        """
        return self.rect.bottom

    @property
    def width(self):
        """
        Return width of Rect object 
        """
        return self.rect.width

    @property
    def height(self):
        """
        Return height of Rect object 
        """
        return self.rect.height

    @property
    def center(self):
        return self.rect.center

    @property
    def centerx(self):
        return self.rect.centerx

    @property
    def centery(self):
        return self.rect.centery

    def draw(self, surface):
        pass

    def move(self, dx, dy):
        self.rect = self.rect.move(dx, dy)

    def update(self):
        """
        Moving an object at a specified speed
        """
        if self.speed == [0, 0]:
            return

        self.move(*self.speed)