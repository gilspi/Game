# -*- coding: utf8 -*-

import random
import sys
import pygame
from GameSettings import WHITE, DARK_PINK, WHITE_PINK, PINK, BLACK
from UIObjects import Button


def terminate():
    """Функция выполняется, когда пользователь завершает сеанс."""
    pygame.quit()
    sys.exit()


def moves_at_the_intersection(*sprites):
    """Принимает спрайты и вызывает метод респавн, класс соответствующего спрайта."""
    for sprite in sprites:
        sprite.generation_random_position()


def collide_past_remove_health(group, arr, sprite):
    """Функция принимает группу спрайтов, список и спрайт.
    В данной части, фунция moves_at_the_intersection(*sprites) будет вызываться с аргументом player.
    """
    if len(arr) >= 1:
        group.remove(arr.pop())
        moves_at_the_intersection(sprite)


def draw_text(surf, score, point=0):
    """Показываает набранное количество очков."""
    font_score = pygame.font.Font(r'Fonts\wayfarers_toybox_regular.ttf', 15)
    font_point = pygame.font.SysFont(r'Fonts\wayfarers_toybox_regular.ttf', 15)
    if point > 0:  # True выводит на экран очки за уничтожения.
        text_point = font_point.render('+' + str(point), True, DARK_PINK)
        surf.blit(text_point, (300, 33))

    text_score = font_score.render(str(score), True, WHITE)
    text_score_w, text_score_h = text_score.get_height(), text_score.get_width()
    text_score_x, text_score_y = 300 - text_score_w // 2, 10
    surf.blit(text_score, (text_score_x, text_score_y))


def draw_boss_hp(surf, x_pos, y_pos, subsurf_hp_width, subsurf_hp_height):
    """Выводит рамку с уровнем жизни над БОССом.
    Два последних аргумента передаются для внутренней подповерхности для смены ее ширины."""
    fill = (0, 255, 0)  # начальная закраска
    hp_rect = pygame.Rect(x_pos+25, y_pos-5, subsurf_hp_width, subsurf_hp_height)
    frame_rect = pygame.Rect(x_pos+22, y_pos-8, 303, 8)
    if hp_rect.width < 200:
        fill = (255, 255, 0)
    if hp_rect.width < 100:
        fill = (255, 0, 0)
    pygame.draw.rect(surf, fill, hp_rect)
    pygame.draw.rect(surf, (255, 255, 255), frame_rect, 1)


def losing(surface):
    """Выводит на экран изображение проигрыша и спрашивает, хочет ли игрок начать заново или хочет выйти из игры.
    Игрок проигрывает, когда столкнется с вражескими объектами 3 раза - потеряет все жизни."""
    game_over = pygame.image.load(r'Screens\game_over_screen.png')
    btn_quit = Button(86, 27, WHITE_PINK, PINK)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                running = False
        surface.fill(BLACK)
        surface.blit(game_over, (0, 0))
        btn_quit.draw(surface, 'Выйти из игры', 510, 4, 6, 7, action=terminate, font_size=11)
        pygame.display.update()


def won(surface):
    you_win = pygame.image.load(r'Screens\you_win.png')
    btn_exit = Button(86, 27, WHITE_PINK, PINK)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        surface.fill(BLACK)
        surface.blit(you_win, (0, 0))
        btn_exit.draw(surface, 'Выйти из игры', 510, 4, 6, 7, action=terminate, font_size=11)
        pygame.display.update()
