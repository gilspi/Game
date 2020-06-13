# -*- coding: utf8 -*-

import random
import pygame
from GameFunction import moves_at_the_intersection, terminate, collide_past_remove_health, draw_text, losing, won, \
    draw_boss_hp
from SpaceBattleObject import Background, Player, Mob, Health, Bullet, BlowingUpAnything, Boss
from GameSettings import WIDTH, HEIGHT, FPS, count, score, point, WHITE_PINK, PINK, BLACK
from UIObjects import Button, display_text_on_the_surface


pygame.init()

# Image upload
icon = pygame.image.load(r'OtherImage\icon.png')

screen_saver_img = pygame.image.load(r'Screens\screen_saver.png')

spaceship_rival_burnt = [pygame.image.load(r'Spaceships\rival\SpaceShipRivalBurnt\spaceship_rival_burnt_1.png'),
                         pygame.image.load(r'Spaceships\rival\SpaceShipRivalBurnt\spaceship_rival_burnt_2.png'),
                         pygame.image.load(r'Spaceships\rival\SpaceShipRivalBurnt\spaceship_rival_burnt_3.png'),
                         pygame.image.load(r'Spaceships\rival\SpaceShipRivalBurnt\spaceship_rival_burnt_4.png')]

explosion = [pygame.image.load(r'Explosion\explosion_1.png'),
             pygame.image.load(r'Explosion\explosion_2.png'),
             pygame.image.load(r'Explosion\explosion_3.png'),
             pygame.image.load(r'Explosion\explosion_4.png'),
             pygame.image.load(r'Explosion\explosion_5.png'),
             pygame.image.load(r'Explosion\explosion_6.png'),
             pygame.image.load(r'Explosion\explosion_7.png'),
             pygame.image.load(r'Explosion\explosion_8.png')]

player_bullet = [pygame.image.load(r'Spaceships\player\bullet\bullet1.png'),
                 pygame.image.load(r'Spaceships\player\bullet\bullet2.png')]

boss_bullet = [pygame.image.load(r'Spaceships\boss\bullet\bullet1.png'),
               pygame.image.load(r'Spaceships\boss\bullet\bullet2.png'),
               pygame.image.load(r'Spaceships\boss\bullet\bullet3.png'),
               pygame.image.load(r'Spaceships\boss\bullet\bullet4.png')]

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Последний полет')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

# Group
all_sprites = pygame.sprite.Group()
boss_game_sprites = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
boss_bullets = pygame.sprite.Group()
mobs = pygame.sprite.Group()

# Objects
mob1 = Mob(random.randrange(0, 150), random.randrange(-85, -10))
mob2 = Mob(random.randrange(247, 350), random.randrange(-270, -170))
mob3 = Mob(random.randrange(447, 506), random.randrange(-470, -355))
boss = Boss(WIDTH // 2 - 175, -210)
player = Player(clock)
d = [Health(13, 10),
     Health(33, 10),
     Health(53, 10)]
bullet = Bullet(player_bullet, player.rect.centerx, player.rect.top)
b_bullet = Bullet(boss_bullet, boss.rect.x, boss.rect.y)
# mob1_bullet = Bullet(rival_bullet, mob1.rect.x, mob1.rect.y)
# mob2_bullet = Bullet(rival_bullet, mob2.rect.x, mob2.rect.y)
# mob3_bullet = Bullet(rival_bullet, mob3.rect.x, mob3.rect.y)
######################################################################

all_sprites.add(Background(0, -600),
                Background(0, 0))
all_sprites.add(player)
all_sprites.add(mob1)
all_sprites.add(mob2)
all_sprites.add(mob3)
all_sprites.add(d)

mobs.add(mob1)
mobs.add(mob2)
mobs.add(mob3)
# Отображает набранное количество очков
draw_text(window, score)

# Все звуки игры
pygame.mixer.music.load(r'Sounds\background.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
destroyed_boss_spaceship = pygame.mixer.Sound(r'Sounds\destroyed_boss.wav')
destroyed_boss_spaceship.set_volume(1)
expl_boss_spaceship = pygame.mixer.Sound(r'Sounds\expl_boss_spaceship.wav')
expl_boss_spaceship.set_volume(0.3)


def initial_splash_screen(surf, img, clock, fps):
    btn_start = Button(162, 50, WHITE_PINK, PINK)
    btn_exit = Button(107, 33, WHITE_PINK, PINK)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        surf.blit(img, (0, 0))  # позиция верхнего левого угла
        btn_start.draw(surf, 'Новая игра', 220, 427, 16, 10, action=game, font_size=25)
        btn_exit.draw(surf, 'Выйти из игры', 245, 511, 7, 9, action=terminate, font_size=14)
        pygame.display.update()
        clock.tick(fps)


def game_boss():
    global d, count, player, score, point, count, player, all_sprites, mob1, mob2, mob3, d, bullet, mobs, player_bullets
    boss = Boss(WIDTH // 2 - 175, -210)
    boss_game_sprites.add(Background(0, -600),
                          Background(0, 0))
    boss_game_sprites.add(boss)
    boss_game_sprites.add(player)
    boss_game_sprites.add(d)
    width = 300
    height = 5
    player.win = False
    player.lose = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.shoot(player_bullet, boss_game_sprites, player_bullets)

        if not player.lose and count >= 1:
            if pygame.sprite.spritecollide(player, boss_bullets, True):
                count -= 1
                if count == 0:
                    player.lose = True
                collide_past_remove_health(boss_game_sprites, d, player)
            if width >= 1:
                hits = pygame.sprite.spritecollide(boss, player_bullets, True)
                for hit in hits:
                    if hit.rect.centerx < 350:
                        blowing_up = BlowingUpAnything(explosion, hit.rect.x - random.randrange(10, 40),
                                                       hit.rect.y - random.randrange(100, 140))
                    else:
                        blowing_up = BlowingUpAnything(explosion, hit.rect.x - random.randrange(50, 100),
                                                       hit.rect.y - random.randrange(70, 100))
                    boss_game_sprites.add(blowing_up)
                    width -= 25
            else:
                player.win = True
        window.fill(BLACK)
        boss_game_sprites.draw(window)
        boss.shoot(boss_bullet, boss_game_sprites, boss_bullets)
        boss_game_sprites.update()
        draw_boss_hp(window, boss.rect.x, boss.rect.y, width, height)
        pygame.display.update()
        clock.tick(FPS)
        if player.win or player.lose:
            if player.win:
                destroyed_boss_spaceship.play()
                pygame.mixer.music.stop()
                won(window)
            else:
                losing(window)
                player.lose = False
                score = 0
                point = 0
                count = 3

                all_sprites.empty()
                mobs.empty()
                player_bullets.empty()

                player = Player(clock)
                mob1 = Mob(random.randrange(0, 150), random.randrange(-85, -10))
                mob2 = Mob(random.randrange(247, 350), random.randrange(-270, -170))
                mob3 = Mob(random.randrange(447, 506), random.randrange(-470, -355))
                d = [Health(13, 10),
                     Health(33, 10),
                     Health(53, 10)]
                bullet = Bullet(player_bullet, player.rect.centerx, player.rect.top)

                all_sprites.add(Background(0, -600),
                                Background(0, 0))
                all_sprites.add(player)
                all_sprites.add(mob1)
                all_sprites.add(mob2)
                all_sprites.add(mob3)
                all_sprites.add(d)

                mobs.add(mob1)
                mobs.add(mob2)
                mobs.add(mob3)
                running = False
                game()


def game():
    global score, point, count, player, all_sprites, mob1, mob2, mob3, d, bullet, mobs, player_bullets
    player.win = False
    player.lose = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                point = 0
                player.shoot(player_bullet, all_sprites, player_bullets)

        if not player.lose and count >= 1:
            if pygame.sprite.collide_mask(player, mob1) or pygame.sprite.collide_mask(player, mob2) \
                    or pygame.sprite.collide_mask(player, mob3):
                moves_at_the_intersection(player)
                count -= 1
                if count == 0:
                    player.lose = True
                collide_past_remove_health(all_sprites, d, player)

            if score <= 5000:  # FIXME ввести константу
                # Прошло проверку, значит игрок еще не набрал нужное количество очков
                hits = pygame.sprite.groupcollide(mobs, player_bullets, False, True)
                for hit in hits:
                    blowing_up = BlowingUpAnything(spaceship_rival_burnt, hit.rect.x, hit.rect.y)
                    all_sprites.add(blowing_up)
                    destruct = random.randrange(200, 300)  # количество добавляемых очков после уничтожения
                    score += destruct
                    point += destruct
                    moves_at_the_intersection(hit)
            else:
                player.win = True

            if pygame.sprite.collide_rect(mob1, mob2):
                moves_at_the_intersection(mob1, mob2)
            if pygame.sprite.collide_rect(mob1, mob3):
                moves_at_the_intersection(mob1, mob3)
            if pygame.sprite.collide_rect(mob2, mob3):
                moves_at_the_intersection(mob2, mob3)

        window.fill(BLACK)
        all_sprites.draw(window)
        all_sprites.update()
        draw_text(window, score, point)
        pygame.display.update()
        clock.tick(FPS)

        if player.lose or player.win:
            if player.lose:
                losing(window)
                player.lose = False

                score = 0
                point = 0
                count = 3

                all_sprites.empty()
                mobs.empty()
                player_bullets.empty()

                player = Player(clock)
                mob1 = Mob(random.randrange(0, 150), random.randrange(-85, -10))
                mob2 = Mob(random.randrange(247, 350), random.randrange(-270, -170))
                mob3 = Mob(random.randrange(447, 506), random.randrange(-470, -355))
                d = [Health(13, 10),
                     Health(33, 10),
                     Health(53, 10)]
                bullet = Bullet(player_bullet, player.rect.centerx, player.rect.top)

                all_sprites.add(Background(0, -600),
                                Background(0, 0))
                all_sprites.add(player)
                all_sprites.add(mob1)
                all_sprites.add(mob2)
                all_sprites.add(mob3)
                all_sprites.add(d)

                mobs.add(mob1)
                mobs.add(mob2)
                mobs.add(mob3)
            else:
                all_sprites.empty()
                mobs.empty()
                player_bullets.empty()
                game_boss()


initial_splash_screen(window, screen_saver_img, clock, FPS)
