"""
The main parameters of game objects (size, coordinates, colors...)
"""

import colors
import random

#screen params
screen_width = 600
screen_height = 400
frame_rate = 60
screen_color = colors.EGGSHELL

up_margin = screen_width*0.07
margin = screen_width*0.05

#field params
field_color = colors.LAVENDERBLUSH4 #OLIVEDRAB4
field_width = screen_width - 2*margin
field_height = screen_height - up_margin - margin
field_x = margin
field_y = up_margin

#gate params
gate_width = 10
gate_height = 60
gate_params = [[field_x, field_height/4 + up_margin - gate_height/2, colors.WHITE, 'player1'],
[field_x, field_height*3/4 + up_margin - gate_height/2, colors.WHITE, 'player1'],
[field_x + field_width - gate_width, field_height/4 + up_margin - gate_height/2, colors.AZURE2, 'player2'],
[field_x + field_width - gate_width, field_height*3/4 + up_margin - gate_height/2, colors.AZURE2, 'player2']]

#ball params
ball_r = 9
ball_x = screen_width/2
ball_y = up_margin + ball_r
ball_colors = [colors.COBALT, colors.MEDIUMPURPLE4, colors.STEELBLUE2, colors.SKYBLUE3, colors.SANDYBROWN, colors.PEACHPUFF3, colors.DARKOLIVEGREEN3]
ball_speeds = [4, 3, 5, 3, 4]

#mad balls params
mad_ball_colors = [colors.MINT, colors.GOLD1, colors.ORANGE1, colors.PINK2, colors.SLATEBLUE1, colors.VIOLET]
mad_ball_speeds = [10, 7, 8, 5, 6, 9]

#shutter params
shutter_width = 10
shutter_height = 60
shutter_y = field_height/2 + up_margin - shutter_height/2
#player 1 shutter (left)
shutter_color_1 = colors.STEELBLUE4
shutter_x_1 = field_x + gate_width + 10
#player 2 shutter (right)
shutter_color_2 = colors.DARKSLATEBLUE
shutter_x_2 = field_x + field_width - gate_width - 10 - shutter_width
shutter_speed = 5

#other params
message_duration = 2
effect_duration = 20
start_lives = 5
loser_score = 10

#button params
button_text_color = colors.WHITE
button_font_name = 'Arial'
button_font_size = 12
button_normal_back_color = colors.MEDIUMPURPLE4
button_hover_back_color = colors.ORANGE #GRAY21
button_pressed_back_color = colors.ORANGE
menu_offset = 10
small_button_w = 100
small_button_h = up_margin/2.7 
button_w = 120
button_h = up_margin/1.7
medium_button_w = 80

button_params = {'PLAY': [screen_width/4-button_w/2-3*menu_offset, up_margin/2 - button_h/2, button_w, button_h, colors.VIOLETRED4], #MAROON4
'QUIT': [screen_width/2 - small_button_w/2, up_margin/4 - small_button_h/2, small_button_w, small_button_h, colors.MEDIUMPURPLE4], 
"RESTART BALLS": [screen_width/2 - small_button_w/2, up_margin*3/4 - small_button_h/2, small_button_w, small_button_h, colors.MEDIUMPURPLE4],
'ADD BALL': [screen_width - margin - 3*menu_offset - 2*medium_button_w, up_margin/2 - button_h/2, medium_button_w, button_h, colors.MEDIUMPURPLE4], 
'ADD BLOCKS': [screen_width - margin - menu_offset - medium_button_w, up_margin/2 - button_h/2, medium_button_w, button_h, colors.MEDIUMPURPLE4]}

#score displays params
score_display_w = 100
score_display_h = up_margin*0.8
score_display_font_name = 'Arial'
score_display_font_size = 15
score_display_text_color = colors.DIMGRAY
score_display_color = colors.GHOSTWHITE
score_display_params = {'player1': [margin + menu_offset, up_margin/2 - score_display_h/2],
'player2': [screen_width - margin - menu_offset - score_display_w, up_margin/2 - score_display_h/2]}

#brick params
brick_w = 15
brick_h = 15
brick_x_limit_down = int(shutter_x_1 + shutter_width + 30+1)
brick_x_limit_up = int(shutter_x_2 - 30+1-brick_w)
brick_y_limit_down = int(up_margin)
brick_y_limit_up = int(up_margin + field_height-brick_h)
brick_colors = [colors.THISTLE1, colors.THISTLE2, colors.THISTLE3, colors.THISTLE, colors.SNOW3]


