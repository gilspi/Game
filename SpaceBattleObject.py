# -*- coding: utf8 -*-

import random
import pygame
from GameSettings import WIDTH, HEIGHT


pygame.mixer.init()
player_shot_sound = pygame.mixer.Sound(r'Sounds\rival_shot.wav')
player_shot_sound.set_volume(0.4)

boss_shot_sound = pygame.mixer.Sound(r'Sounds\rival_shot.wav')
boss_shot_sound.set_volume(0.4)

explosions = [pygame.mixer.Sound(r'Sounds\expl_rival_spaceship.wav'),
              pygame.mixer.Sound(r'Sounds\expl_rival_spaceship_2.wav')]


class Background(pygame.sprite.Sprite):
    """Класс заднего фона.
    Особого ничего здесь нет, один метод отвечающий за движение и создание эффекта бесконечности.
    """

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(r'screens\background.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = 2

    def update(self):
        """Метод движения background'а.
        Логические проверки, т. к. в главном файле загружается два изображения!
        С помощью этих проверок создается эффект "бесконечного" космоса!
        """
        self.rect = self.rect.move(self.vx, self.vy)
        if self.rect.y > HEIGHT:
            self.rect.y = -600


class Health(pygame.sprite.Sprite):
    """Класс объекта здоровья.
    Показ и удаление изображения здоровья при столкновении с вражеским объектом.
    """

    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(r'OtherImage\hp.png')
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos


class Player(pygame.sprite.Sprite):
    """Класс объекта главного героя! Загрузка изображения; генерация положения после столкновений с вражескими
    объектами; проверка положения героя для того, чтобы убедиться, что он не вышел допустимые грацниы за границы!
    """

    def __init__(self, clock):
        super().__init__()
        self.clock = clock
        self.lose = False  # Если проиграл True и игра заканчивается
        self.win = False  # Если победил, то True и должен появляться Босс
        self.left = False
        self.right = False
        self.counter = 0  # Переменная отвечающая за количество смены кадров
        self.move_left = [
            pygame.image.load(r'Spaceships\player\SpaceShipPlayerLeft\spaceship_player_left1.png'),
            pygame.image.load(r'Spaceships\player\SpaceShipPlayerLeft\spaceship_player_left2.png')]
        self.move_right = [
            pygame.image.load(r'Spaceships\player\SpaceShipPlayerRight\spaceship_player_right1.png'),
            pygame.image.load(r'Spaceships\player\SpaceShipPlayerRight\spaceship_player_right2.png')]
        self.standing = [
            pygame.image.load(r'Spaceships\player\SpaceShipPlayerStraight\spaceship_player_straight1.png'),
            pygame.image.load(r'Spaceships\player\SpaceShipPlayerStraight\spaceship_player_straight2.png')]
        self.image = self.standing[0]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 3
        self.vx = 3
        self.vy = 0
        self.cooldown = 700  # перезарядку
        self.last_update = pygame.time.get_ticks()

    def update(self):
        """Обновление положения главного героя!
        Значения вычисляются таким образом, если текущее положение больше левой или меньше правой,
        то персонаж не может двигаться дальше! Выполняется анимация, после проверки нескольких условий.
        """
        keys = pygame.key.get_pressed()
        self.animation()
        if keys[pygame.K_LEFT]:
            if self.rect.x > 1:
                self.rect.x -= self.vx
                self.left = True
                self.right = False
        elif keys[pygame.K_RIGHT]:
            if self.rect.x < WIDTH - self.image.get_width():
                self.rect.x += self.vx
                self.left = False
                self.right = True
        else:
            self.right = False
            self.left = False

    def animation(self):
        """Спрайт передается для получения позиции этого спрайта."""
        if self.counter == 32:
            self.counter = 0

        if self.left:
            self.image = self.move_left[self.counter // 16]
            self.counter += 1
        elif self.right:
            self.image = self.move_right[self.counter // 16]
            self.counter += 1
        else:
            self.image = self.standing[self.counter // 16]
            self.counter += 1

    def shoot(self, list, group_a, group_b):
        """Метод выстела.
        При нажатии на пробел производится выстрел,
        генерирует снаряд в позиции главного объекта.
        """
        now = pygame.time.get_ticks()
        if now - self.last_update > self.cooldown:
            self.last_update = now
            bullet = Bullet(list, self.rect.centerx, self.rect.top, -10)
            group_a.add(bullet)
            group_b.add(bullet)
            player_shot_sound.play()

    def generation_random_position(self):
        """Происходит генерация случайного пололжения главного героя!
        После столкновения с вражеским объектами, если такое произошло,
        генерируется случайное положение в нижней части экрана
        """
        self.rect.x = random.randrange(0, WIDTH - self.image.get_width())
        self.rect.y = HEIGHT - self.image.get_height() - 3


class Bullet(pygame.sprite.Sprite):
    """ Класс снаряда.
    Отвечает за генерацию снаряда в месте, где находится главный персонаж.
    За удаление снаряда, когда он вылетел за границы.
    """

    def __init__(self, list, x, y, vy=5):
        super().__init__()
        self.shot_motion = list
        self.shot = False  # отвечает за анимацию
        self.counter = 0
        self.image = self.shot_motion[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.vy = vy

    def update(self):
        self.shot = True  # Переменная True, когда игрок нажал на пробел(в главном цикле)
        self.rect = self.rect.move(0, self.vy)
        self.animation()
        # kill если вышло за верхнюю границу экрана
        if self.rect.bottom < 0:
            self.kill()

    def animation(self):
        if self.counter == 32:
            self.counter = 0

        if self.shot:
            self.image = self.shot_motion[self.counter // 16]
            self.counter += 1


class Mob(pygame.sprite.Sprite):
    """Класс вражеских героев.
    Методы отвечающие за генерацию случайного положения и за движения!
    """

    def __init__(self, x, y):
        super().__init__()
        self.traffic = [pygame.image.load(r'Spaceships\rival\SpaceShipRival\spaceship_rival_2.png'),
                        pygame.image.load(r'Spaceships\rival\SpaceShipRival\spaceship_rival_4.png')]  # обычное движение моба
        self.image = self.traffic[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = 4
        self.counter = 0  # счетчик для смены кадров
        self.straight_ahead = False

    def update(self):
        """Движение вражеских героев, как только выходят за нижнюю границу,
        выполняется спавн в новое случаное положение.
        """
        self.rect = self.rect.move(self.vx, self.vy)
        self.animation()
        if self.rect.y > HEIGHT:
            self.generation_random_position()

    def animation(self):
        """Целочисленное деление на 16 дает возможность менять кадры реже!"""
        if self.counter == 32:
            self.counter = 0

        if self.straight_ahead:
            self.image = self.traffic[self.counter // 16]
            self.counter += 1

    def generation_random_position(self):
        """ Обычная генерация случайного положения, с учетом правой границы."""
        self.rect.x = random.randrange(0, WIDTH - self.image.get_width())
        self.rect.y = random.randrange(-700, -(100 + self.image.get_height()))


class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(r'Spaceships\boss\boss.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 2
        self.vy = 2
        self.counter = 0
        self.last_update = pygame.time.get_ticks()
        self.cooldown = 2500

    def update(self):
        """Здесь происходит обновления позиции БОССа.
        Появляется он сверху и двигается только по вертикали,
        только после того, как игрок наберет определенное кол-во очков.
        Также он отталкивается от границы, когда соприкасается с ней."""
        if self.rect.y < 0:
            self.rect = self.rect.move(0, 3)
        else:
            self.rect.x += self.vx
            if self.rect.x > WIDTH - self.image.get_width() or self.rect.x < 0:
                self.vx = -self.vx
            self.rect.y += self.vy
            if self.rect.y > (HEIGHT // 2 - self.image.get_height() // 2) or self.rect.y < 0:
                self.vy = -self.vy

    def shoot(self, list, group_a, group_b):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.cooldown:
            self.last_update = now
            bullet = Bullet(list, self.rect.centerx, self.rect.bottom, 10)
            group_a.add(bullet)
            group_b.add(bullet)
            boss_shot_sound.play()


class BlowingUpAnything(pygame.sprite.Sprite):
    def __init__(self, list, x, y):
        """list передается для того, чтобы можно было анимировать что-то определенное."""
        super().__init__()
        self.smth = list
        self.image = self.smth[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.counter = 0
        self.last_update = pygame.time.get_ticks()
        self.rate = 50  # определяет скорость

    def update(self):
        now = pygame.time.get_ticks()  # начинается, когда вызывается метод
        if now - self.last_update > self.rate:
            self.last_update = now
            self.counter += 1
            expl = random.choice(explosions)
            expl.set_volume(0.05)
            if self.counter == len(self.smth):
                self.kill()
            else:
                self.image = self.smth[self.counter]
            expl.play()
