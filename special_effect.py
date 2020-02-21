"""
Dictionary of special effects.
---
Словарь спецэффектов.
"""

import colors
import pygame
import config as c


special_effects = {
    'long_shutter': (colors.MINT, 
    lambda x: x.change_shutter_size('long'),
    lambda x: x.change_shutter_size('original')),
   'fast_ball': (colors.TAN3,
    lambda x: x.change_ball_speed(5), lambda x: x.change_ball_speed(-5)),
    'short_shutter': (colors.GRAY21, 
    lambda x: x.change_shutter_size('short'),
    lambda x: x.change_shutter_size('original')),
    'add_score': (colors.MIDNIGHTBLUE, 
    lambda x: x.change_player_score(1),
    lambda x: x.change_player_score(0)),
    'fast_shutter': (colors.MANGANESEBLUE, 
    lambda x: x.change_shutter_size('fast'),
    lambda x: x.change_shutter_size('original')),
    'slow_shutter': (colors.DEEPPINK4, 
    lambda x: x.change_shutter_size('slow'),
    lambda x: x.change_shutter_size('original')),
    'ball_hall': (colors.BANANA, 
    lambda x: x.ball_hall_start(),
    lambda x: x.ball_hall_stop()),

}
 