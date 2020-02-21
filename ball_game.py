"""
The main class of the game that defines the display, game objects, methods, rules, etc.
---
Основной класс игры, определяющий отображение, игровые объекты, методы, правила и т.д.
"""

import pygame
import time
import random
from datetime import datetime, timedelta

import colors
import config as c

from game import Game
from gate import Gate
from ball import Ball
from shutter import Shutter_left, Shutter_right
from text_object import TextObject
from button import Button
from score_display import ScoreDisplay
from special_effect import special_effects

class Ballgame(Game):
    def __init__ (self):
        Game.__init__(self, 'Ball game', c.screen_width, c.screen_height, c.frame_rate)

        self.ball = None
        self.balls = []
        self.ball_number = 1

        self.gates = []
        self.bricks = []

        self.shutter_1 = None
        self.shutter_2 = None
        self.shutters ={'player1': [], 'player2': []}

        self.score_display_1 = None
        self.score_display_2 = None
        self.score_label_player_1 = None
        self.score_label_player_2 = None

        self.field = None
        self.menu_buttons = []
        self.lives = {'player1': c.start_lives, 'player2': c.start_lives}
        self.scores = {'player1': 0, 'player2': 0}
        self.start_level = False
        self.is_game_running = False

        self.reset_effects = None
        self.effect_start_times = None
        self.loser = None
        self.effected_players = None
        self.effected_player_to_change = None
        self.ball_index_to_change = 0

    # Метод для создания и вывода сообщения игрокам
    def show_message(self, text, color=colors.WHITE, font_name='Arial', font_size=20, centralized=False):
        message = TextObject(c.screen_width // 2, c.screen_height // 2, lambda: text, color, font_name, font_size)
        self.draw()
        message.draw(self.surface, centralized)
        pygame.display.update()
        time.sleep(c.message_duration)

    # Create balls
    def create_balls(self, special_effect_on = True, mad_balls = 0):

        total_ball_number = self.ball_number+mad_balls
        self.balls = []
        self.reset_effects =[None]*(total_ball_number)
        self.effected_players =[None]*(total_ball_number)
        self.effect_start_times =[None]*(total_ball_number)
        
        for i in range(total_ball_number):
            effect = None
            if mad_balls == 0:
                ball_color = c.ball_colors[random.randint(0,5)]
                x = random.randint(-4, 4)
                while x == 0 or abs(x) < 2:
                    x = random.randint(-4, 4)
                speed = (x, c.ball_speeds[i % 5])
            else:
                ball_color = c.mad_ball_colors[i % 6]
                x = random.randint(-10, 10)
                while x == 0 or abs(x) < 4:
                    x = random.randint(-10, 10)
                speed = (x, c.mad_ball_speeds[i % 6])

            if special_effect_on:
                special_effect_index = random.randint(1, 11)
                #special_effect_index = 6
                if special_effect_index < len(special_effects):
                    x = list(special_effects.values())[special_effect_index]
                    ball_color = x[0]
                    effect = x[1:]
                    #print(ball_color, effect[0])

            ball = Ball(c.ball_x, c.ball_y, c.ball_r, ball_color, speed, effect)
            self.objects.append(ball)
            self.balls.append(ball)

    # Create gates
    def create_gates(self):
        for param in c.gate_params:
            gate = Gate(param[0], param[1], c.gate_width, c.gate_height, param[2], param[3])
            self.objects.append(gate)
            self.gates.append(gate)

    # Create field
    def create_field(self):
        self.field = Gate(c.field_x, c.field_y, c.field_width, c.field_height, c.field_color, '')
        self.objects.append(self.field)

    # Create shutters for player1 and player2
    def create_shutters(self):
        shutter_1 = Shutter_left(c.shutter_x_1, c.shutter_y, c.shutter_width, c.shutter_height, c.shutter_color_1, c.shutter_speed)
        self.keydown_handlers[pygame.K_w].append(shutter_1.handle)
        self.keydown_handlers[pygame.K_s].append(shutter_1.handle)
        self.keyup_handlers[pygame.K_w].append(shutter_1.handle)
        self.keyup_handlers[pygame.K_s].append(shutter_1.handle)
        self.shutter_1 = shutter_1
        self.objects.append(self.shutter_1)
        self.shutters['player1'].append(self.shutter_1)

        shutter_2 = Shutter_right(c.shutter_x_2, c.shutter_y, c.shutter_width, c.shutter_height, c.shutter_color_2, c.shutter_speed)
        self.keydown_handlers[pygame.K_UP].append(shutter_2.handle)
        self.keydown_handlers[pygame.K_DOWN].append(shutter_2.handle)
        self.keyup_handlers[pygame.K_UP].append(shutter_2.handle)
        self.keyup_handlers[pygame.K_DOWN].append(shutter_2.handle)
        self.shutter_2 = shutter_2
        self.objects.append(self.shutter_2)
        self.shutters['player2'].append(self.shutter_2)

    # Создание блоков (функция для кнопки)
    def create_bricks(self):
        brick_number = random.randint(1,4)
        for i in range(brick_number):
            cross = False
            x = random.randint(c.brick_x_limit_down, c.brick_x_limit_up)
            y = random.randint(c.brick_y_limit_down, c.brick_y_limit_up)
            brick = Gate(x, y, c.brick_w, c.brick_h, c.brick_colors[i], '')
            if len(self.bricks):
                for gate in self.bricks:
                    cross = brick.rect.colliderect(gate.rect)
            if not cross:
                self.objects.append(brick)
                self.bricks.append(brick)

    # Отмена дейсвтия эффекта мяча по его индексу
    def reset_effect_action(self, index):
        self.effected_player_to_change = self.effected_players[index]
        self.reset_effects[index](self)
        self.reset_effects[index] = None 
        self.effected_players[index] = None
        #print('Reset!!!!')
 
    # Метод для изменения скорости мяча для эффекта
    def change_ball_speed(self, dy):
        self.balls[self.ball_index_to_change].speed = ( self.balls[self.ball_index_to_change].speed[0]+dy,  self.balls[self.ball_index_to_change].speed[1]+dy)

    # Метод для изменения количества жизней игрока (не используется)
    def change_player_live(self, delta):
        self.lives[self.effected_player_to_change] -= delta
        if self.lives[self.effected_player_to_change] == 0:
            self.loser = str(self.effected_player_to_change)
            self.game_over = True

    # Метод для изменения счета игрока для эффекта
    def change_player_score(self, delta):
        self.scores[self.effected_player_to_change] += delta
        if self.scores[self.effected_player_to_change] == c.loser_score:
            self.game_over = True
            self.loser = str(self.effected_player_to_change)

    # Метод для изменения свойств шаттера для эффекта
    def change_shutter_size(self, marker):
        if marker == 'long':
            self.shutters[self.effected_player_to_change][0].rect.inflate_ip(0, self.shutters[self.effected_player_to_change][0].rect.height/2)
            return
        elif marker == 'short':
            self.shutters[self.effected_player_to_change][0].rect.inflate_ip(0, - self.shutters[self.effected_player_to_change][0].rect.height/2)
            return
        elif marker == 'slow':
            self.shutters[self.effected_player_to_change][0].offset -= 4
            return
        elif marker == 'fast':
            self.shutters[self.effected_player_to_change][0].offset += 4
            return
        self.shutters[self.effected_player_to_change][0].rect.inflate_ip(0, - self.shutters[self.effected_player_to_change][0].rect.height + c.shutter_height)
        self.shutters[self.effected_player_to_change][0].offset = c.shutter_speed

    # Метод для эффекта ball madness
    def ball_hall_start(self):
        self.show_message('ATTENTION!!! BALL MADNESS!!!', centralized=True)
        for index in range(len(self.balls)):
            if self.reset_effects[index] is not None:
                self.reset_effect_action(index)
            ball = self.balls[index]
            self.objects.remove(ball)
        self.create_balls(special_effect_on = False, mad_balls = 7)

    def ball_hall_stop(self):
        pass

    # Создание кнопок и меню
    def create_menu(self):
        def on_play(button):
            self.objects.remove(self.menu_buttons[0]) # remove PLAY button
            self.objects.remove(self.menu_buttons[-1]) # remove ADD BLOCKS button
            self.objects.remove(self.menu_buttons[-2]) # remove ADD BALL button
            self.is_game_running = True
            self.start_level = True
            self.create_balls()

        def on_quit(button):
            self.game_over = True
            self.is_game_running = False

        def on_restart_ball(button):
            for index in range(len(self.balls)):
                if self.reset_effects[index] is not None:
                    self.reset_effect_action(index)
                ball = self.balls[index]
                self.objects.remove(ball)
                #self.balls.remove(ball)

            self.create_balls()

        def on_add_ball(button):
            self.ball_number += 1

        def on_add_blocks(button):
            self.create_bricks()

        actions = {'PLAY': on_play, 'QUIT': on_quit, "RESTART BALLS": on_restart_ball, 'ADD BALL': on_add_ball, 'ADD BLOCKS': on_add_blocks}
        for key, value in actions.items():
            but = Button(c.button_params[key][0], c.button_params[key][1], c.button_params[key][2], c.button_params[key][3], c.button_params[key][4], str(key), value)
            self.objects.append(but)
            self.menu_buttons.append(but)
            self.mouse_handlers.append(but.handle_mouse_event)

    # Создание окон для отображения счета игроков    
    def create_score_displays(self):
        self.score_display_1 = ScoreDisplay(c.score_display_params['player1'][0], c.score_display_params['player1'][1])
        self.score_label_player_1 = TextObject(self.score_display_1.centerx, self.score_display_1.centery - self.score_display_1.height/4, lambda: str(self.scores['player1']), c.score_display_text_color, c.score_display_font_name, c.score_display_font_size)
        self.objects.append(self.score_display_1)
        self.objects.append(self.score_label_player_1)

        self.score_display_2 = ScoreDisplay(c.score_display_params['player2'][0], c.score_display_params['player2'][1])
        self.score_label_player_2 = TextObject(self.score_display_2.centerx, self.score_display_2.centery - self.score_display_2.height/4, lambda: str(self.scores['player2']), c.score_display_text_color, c.score_display_font_name, c.score_display_font_size)
        self.objects.append(self.score_display_2)
        self.objects.append(self.score_label_player_2)

    # Создание основных игровых объектов
    def create_objects(self):
        self.create_field()
        self.create_gates()
        #self.create_balls()
        self.create_shutters()
        self.create_menu()

    # Метод для отслеживания соударений шарика и игровых объектов
    def handle_ball_collision(self):
        ball_index_to_remove =[]

        def crossing(obj, ball, c_l = 0, c_r = 0, c_t = 0, c_b = 0):
            """
            Функция, определяющая пересечение между объектом и мячом.
            Возвращает None или сторону пересечения.
            """
            #gap_l =c.ball_r*c_l
            #gap_r =c.ball_r*c_r
            #gap_t =c.ball_r*c_t
            #gap_b =c.ball_r*c_b

            obj_edges = {'left': pygame.Rect(obj.left, obj.top, 1, obj.height),
            'right': pygame.Rect(obj.right, obj.top, 1, obj.height),
            'top': pygame.Rect(obj.left, obj.top, obj.width, 1),
            'bottom': pygame.Rect(obj.left, obj.bottom, obj.width, 1)}
            crossing_sides = set()

            for key, value in obj_edges.items():
                if ball.rect.colliderect(value):
                    crossing_sides.add(key)

            #no crossings
            if not crossing_sides:
                return None

            #only one crossing
            if len(crossing_sides) == 1:
                return list(crossing_sides)[0]

            #more than one crossings
            if 'right' in crossing_sides:
                if ball.centery <= obj.top:
                    return 'top'
                if ball.centery >= obj.bottom:
                    return 'bottom'
                if ball.centerx < obj.left:
                    return 'left'
                else:
                    return 'right'

            if 'left' in crossing_sides:
                if ball.centery <= obj.top:
                    return 'top'
                if ball.centery >= obj.bottom:
                    return 'bottom'
                if ball.centerx > obj.right:
                    return 'right'
                else:
                    return 'left'

        # Проверка каждого из шариков на столкновение с игровыми объектами и изменение поведения
        for index in range(len(self.balls)):
            ball = self.balls[index]
            ball_speed = list(ball.speed)

            # Столкновение с шаттером player
            for player, shutter in self.shutters.items():
                side = crossing(shutter[0], ball)
                if side is not None:
                    if side == 'right' or side == 'left':
                        ball.speed = (-ball_speed[0], ball_speed[1])
                    else:
                        ball.speed = (ball_speed[0], -ball_speed[1])
                    # Специальные эффекты мяча
                    # Если у мяча есть эффект и это первое соударение
                    if ball.special_effect is not None and self.reset_effects[index] is None:
                        self.effected_players[index] = player
                        self.effect_start_times[index] = datetime.now()
                        self.effected_player_to_change = self.effected_players[index]
                        self.ball_index_to_change = index
                        ball.special_effect[0](self)
                        self.reset_effects[index] = ball.special_effect[1]

            # Столкновение с верхней/нижней границами поля
            if ball.rect.top < self.field.rect.top or ball.rect.bottom > self.field.rect.bottom:
                ball.speed = (ball_speed[0], -ball_speed[1])

            # Столкновение со стенами
            if ball.rect.left < self.field.rect.left or ball.rect.right > self.field.rect.right:
                ball.speed = (-ball_speed[0], ball_speed[1])

            # Столкновение с блоками
            if len(self.bricks) > 0:
                for brick in self.bricks:
                    side = crossing(brick, ball)
                    if side is not None:
                        if side == 'right' or side == 'left':
                            ball.speed = (-ball_speed[0], ball_speed[1])
                        else:
                            ball.speed = (ball_speed[0], -ball_speed[1])

            # Столкновение с воротами игроков
            for gate in self.gates:
                side = crossing(gate, ball)
                if side is not None:
                    self.scores[gate.player] += 1
                    if self.scores[gate.player] == c.loser_score:
                        self.game_over = True
                        self.loser = str(gate.player)
                    else:
                        ball_index_to_remove.append(index)
        
        # Удаление шариков, попавших в ворота игроков
        if len(ball_index_to_remove) > 0:
            for i in range(len(ball_index_to_remove)-1, -1, -1):
                index = ball_index_to_remove[i]
                if self.reset_effects[index] is not None:
                    self.reset_effect_action(index)
                ball_to_remove = self.balls[index]
                self.objects.remove(ball_to_remove)
                self.balls.remove(ball_to_remove)
                self.reset_effects[index] = None
                self.effected_players[index] = None
                self.effect_start_times[index] = None
            ball_index_to_remove = []
        
        # Проверка на оставшееся количество шариков
        if len(self.balls) == 0:
            self.create_balls()
            return

    def update(self):
        if not self.is_game_running:
            return

        if self.start_level:
            self.start_level = False
            self.show_message('GET READY!', centralized=True)
            self.scores['player1'] = 0
            self.scores['player2'] = 0
            self.lives['player1'] = c.start_lives
            self.lives['player2'] = c.start_lives
            self.create_score_displays()

        self.handle_ball_collision()

        # Reset one of the special effects if needed
        for index in range(len(self.reset_effects)):
            if self.reset_effects[index] is not None and self.effect_start_times[index] is not None:
                if datetime.now() - self.effect_start_times[index] >= timedelta(seconds=c.effect_duration):
                    self.reset_effect_action(index)

        super().update()

        if self.game_over:
            self.show_message('GAME OVER! {} loses...'.format(self.loser), centralized=True)

    # Main
    def start_game(self):
        self.create_objects()
        self.run()
            
def main():
    Ballgame().start_game()

if __name__ == '__main__':
    main()

