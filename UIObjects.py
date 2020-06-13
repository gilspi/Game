# -*- coding: utf8 -*-

import pygame
from GameSettings import WHITE


def display_text_on_the_surface(surface, message, font_size, color, x, y, from_the_side_border, from_the_up_border):
    font = pygame.font.Font(r'Fonts\arial.ttf', font_size)
    text = font.render(str(message), True, color)
    surface.blit(text, (x + from_the_side_border, y + from_the_up_border))


class Button:
    def __init__(self, width, height, active, inactive):
        self.width = width
        self.height = height
        self.active = active
        self.inactive = inactive

    def draw(self, surface, message, x, y, side_border, up_border, action=None, font_size=10):
        """Создает кнопку на указанной поверхности. На кнопке создается текст.
        X и Y задают положение верхнего левого угла кнопки. Action обозначает,
        будет ли выполняться какое-либо действие при нажатии на кнопку.
        Положение курсора мыши нужно для проверки - попал ли он в 'площадь' кнопки."""
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()

        if (x < mouse_pos[0] < x + self.width) and (y < mouse_pos[1] < y + self.height):
            pygame.draw.rect(surface, self.active, (x, y, self.width, self.height))
            pygame.time.delay(50)
            if mouse_press[0] and action is not None:
                action()
        else:
            pygame.draw.rect(surface, self.inactive, (x, y, self.width, self.height))
        display_text_on_the_surface(surface, message, font_size, WHITE, x, y, side_border, up_border)
