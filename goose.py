import pygame as pg
from pygame.constants import *
from random import randint
from os import listdir

pg.init()

FPS = pg.time.Clock()

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (181, 230, 235)
YELLOW = (255, 255, 0)
ORANGE = (255, 148, 0)

IMAGES_PATH = 'player_img'
START_SCREEN_WIDTH = 900
START_SCREEN_HEIGHT = 400
START_FONT = 'Verdana'
START_FONT_SIZE = int(START_SCREEN_WIDTH/35)
DEFEAT_TEXT = ('GAME OVER !', 'PRESS SPACE TO TRY AGAIN !', 'HAVE A NICE TIME :)')
PAUSE_TEXT = ('PAUSE', 'PRESS P TO CONTINUE')

START_SCORE = 0
START_PLAYER_SIZE = int(START_SCREEN_WIDTH/20)
START_PLAYER_LIFE = 3
START_PLAYER_SPEED = 4
START_ENEMY_MIN_SPEED = 2
START_ENEMY_MAX_SPEED = 3
START_ENEMY_MIN_SIZE = 20
START_ENEMY_MAX_SIZE = 30

screen = width, height = START_SCREEN_WIDTH, START_SCREEN_HEIGHT
main_surface = pg.display.set_mode(screen)

font_size = START_FONT_SIZE
font = pg.font.SysFont(START_FONT, font_size, 1, 1)

heart_icon = pg.transform.scale(pg.image.load('life_bonus.png').convert_alpha(), (font_size, font_size))
speed_icon = pg.transform.scale(pg.image.load('speed_bonus.png').convert_alpha(), (font_size, font_size))

bg_ifdefeat = pg.transform.scale(pg.image.load('background_ifdefeat.png').convert(), screen)
bg = pg.transform.scale(pg.image.load('background.png').convert(), screen)
bgX1 = 0
bgX2 = bg.get_width()
bg_speed = 1

image_index = 0
player_size = START_PLAYER_SIZE
player_images = [pg.transform.scale(pg.image.load(IMAGES_PATH + '/' + file).convert_alpha(), (player_size*2, player_size)) for file in listdir(IMAGES_PATH)]
player = player_images[0]
player_rect = pg.Rect(width/2, height/2, *player.get_size())
player_speed = START_PLAYER_SPEED
player_life = START_PLAYER_LIFE
score = START_SCORE

enemy_min_size = START_ENEMY_MIN_SIZE
enemy_max_size = START_ENEMY_MAX_SIZE
enemy_min_speed = START_ENEMY_MIN_SPEED
enemy_max_speed = START_ENEMY_MAX_SPEED

def create_enemy():
    enemy_size = randint(enemy_min_size, enemy_max_size)
    enemy_speed = randint(enemy_min_speed, enemy_max_speed)
    enemy = pg.transform.scale(pg.image.load('enemy.png').convert_alpha(), (enemy_size*2, enemy_size))
    enemy_rect = pg.Rect(width + enemy_size + enemy_speed, randint(0, height - enemy_size), *enemy.get_size())
    return [enemy, enemy_rect, enemy_speed]

def create_life_bonus():
    life_bonus_size = randint(width/25, width/25 + 20)
    life_bonus_speed = randint(2, 5)
    life_bonus = pg.transform.scale(pg.image.load('life_bonus.png').convert_alpha(), (life_bonus_size, life_bonus_size))
    life_bonus_rect = pg.Rect(randint(0, width - life_bonus_size), 0 - life_bonus_size - life_bonus_speed, *life_bonus.get_size())
    return [life_bonus, life_bonus_rect, life_bonus_speed]

def create_score_bonus():
    score_bonus_size = randint(width/25, width/25 + 20)
    score_bonus_speed = randint(2, 5)
    score_bonus = pg.transform.scale(pg.image.load('score_bonus.png').convert_alpha(), (score_bonus_size, score_bonus_size*2))
    score_bonus_rect = pg.Rect(randint(0, width - score_bonus_size), 0 - score_bonus_size - score_bonus_speed, *score_bonus.get_size())
    return [score_bonus, score_bonus_rect, score_bonus_speed]

def create_speed_bonus():
    speed_bonus_size = randint(width/25, width/25 + 20)
    speed_bonus_speed = randint(2, 5)
    speed_bonus = pg.transform.scale(pg.image.load('speed_bonus.png').convert_alpha(), (speed_bonus_size, speed_bonus_size))
    speed_bonus_rect = pg.Rect(randint(0, width - speed_bonus_size), 0 - speed_bonus_size - speed_bonus_speed, *speed_bonus.get_size())
    return [speed_bonus, speed_bonus_rect, speed_bonus_speed]

player_name = 'unknown'
        
enemies = []
life_bonuses = []
score_bonuses = []
speed_bonuses = []

CREATE_ENEMY_EVENT = pg.USEREVENT + 1
pg.time.set_timer(CREATE_ENEMY_EVENT, randint(500, 5500))
CREATE_LIFE_BONUS_EVENT = pg.USEREVENT + 5
pg.time.set_timer(CREATE_LIFE_BONUS_EVENT, randint(5500, 40000))
CREATE_SCORE_BONUS_EVENT = pg.USEREVENT + 3
pg.time.set_timer(CREATE_SCORE_BONUS_EVENT, randint(5500, 10000))
CREATE_SPEED_BONUS_EVENT = pg.USEREVENT + 4
pg.time.set_timer(CREATE_SPEED_BONUS_EVENT, randint(5500, 20000))
CREATE_CHANGE_PLAYER_IMAGES_EVENT = pg.USEREVENT + 2
pg.time.set_timer(CREATE_CHANGE_PLAYER_IMAGES_EVENT, 120)

is_working = True
is_defeat = False
is_pause = False

while is_working:

    FPS.tick(60)
    pressed_keys = pg.key.get_pressed()

    if is_defeat:

        is_pause = False

        for event in pg.event.get():
            if event.type == QUIT:
                is_working = False
                
        if pressed_keys[K_SPACE]: is_defeat = False
            
        enemies.clear()
        life_bonuses.clear()
        score_bonuses.clear()
        speed_bonuses.clear()
        player_speed = START_PLAYER_SPEED
        player_life = START_PLAYER_LIFE
        enemy_min_speed = START_ENEMY_MIN_SPEED
        enemy_max_speed = START_ENEMY_MAX_SPEED
        enemy_min_size = START_ENEMY_MIN_SIZE
        enemy_max_size = START_ENEMY_MAX_SIZE
        bg_speed = 1

        main_surface.blit(bg_ifdefeat, (0, 0))
        main_surface.blit(player, player_rect)
        main_surface.blit(font.render(str(DEFEAT_TEXT[0]), True, BLACK), (13*font_size, height/2 - 3*font_size))
        main_surface.blit(font.render(str(DEFEAT_TEXT[1]), True, BLACK), (8*font_size, height/2 - font_size))
        main_surface.blit(font.render(str(DEFEAT_TEXT[2]), True, BLACK), (11*font_size, height/2))

        #main_surface.blit(font.render(str(score), True, ORANGE), (width/2, height - 3*font_size))

        if score > 0:
            file = open("score.txt", "a")
            file.write(player_name + ' ' + str(score) + '\n')
            file.close()
            score = START_SCORE

    elif is_pause:

        for event in pg.event.get():
            if event.type == QUIT:
               is_working = False
            
        if pressed_keys[K_p]: 
            is_pause = False

        main_surface.blit(player, player_rect)
        main_surface.blit(font.render(str(PAUSE_TEXT[0]), True, BLACK), (15*font_size, height/2 - 3*font_size))
        main_surface.blit(font.render(str(PAUSE_TEXT[1]), True, BLACK), (10*font_size, height/2 - font_size))
        main_surface.blit(heart_icon, (font_size, 0))
        main_surface.blit(font.render(str(player_life), True, RED), (2*font_size, 0))
        main_surface.blit(speed_icon, (4*font_size, 0))
        main_surface.blit(font.render(str(player_speed), True, BLUE), (5*font_size, 0))
        main_surface.blit(font.render(str(score), True, ORANGE), (10*font_size, 0))

    else:

        for event in pg.event.get():
            if event.type == QUIT:
                is_working = False
            if event.type == CREATE_ENEMY_EVENT:
                enemies.append(create_enemy())
            if event.type == CREATE_LIFE_BONUS_EVENT:
                life_bonuses.append(create_life_bonus())
            if event.type == CREATE_SCORE_BONUS_EVENT:
                score_bonuses.append(create_score_bonus())
            if event.type == CREATE_SPEED_BONUS_EVENT:
                speed_bonuses.append(create_speed_bonus())
            if event.type == CREATE_CHANGE_PLAYER_IMAGES_EVENT:
                image_index += 1
                if image_index == len(player_images):
                    image_index = 0
                player = player_images[image_index]

        bgX1 -= bg_speed
        bgX2 -= bg_speed

        if bgX1 < -bg.get_width():
            bgX1 = bg.get_width()
        if bgX2 < -bg.get_width():
            bgX2 = bg.get_width()

        main_surface.blit(bg, (bgX1, 0))
        main_surface.blit(bg, (bgX2, 0))
        main_surface.blit(player, player_rect)
        main_surface.blit(heart_icon, (font_size, 0))
        main_surface.blit(font.render(str(player_life), True, RED), (2*font_size, 0))
        main_surface.blit(speed_icon, (4*font_size, 0))
        main_surface.blit(font.render(str(player_speed), True, BLUE), (5*font_size, 0))
        main_surface.blit(font.render(str(score), True, ORANGE), (10*font_size, 0))

        for enemy in enemies:
            enemy[1] = enemy[1].move(-enemy[2], 0)
            main_surface.blit(enemy[0], enemy[1])
            if enemy[1].right <= 0 - enemy[2]:
                enemies.pop(enemies.index(enemy))
            if player_rect.colliderect(enemy[1]):
                if player_life > 1:
                    enemies.pop(enemies.index(enemy))
                    player_life = player_life - 1
                else: is_defeat = True

        for life_bonus in life_bonuses:
            life_bonus[1] = life_bonus[1].move(0, life_bonus[2])
            main_surface.blit(life_bonus[0], life_bonus[1])
            if life_bonus[1].top >= height + life_bonus[2]:
                life_bonuses.pop(life_bonuses.index(life_bonus))
            if player_rect.colliderect(life_bonus[1]):
                life_bonuses.pop(life_bonuses.index(life_bonus))
                player_life = player_life + 1

        for score_bonus in score_bonuses:
            score_bonus[1] = score_bonus[1].move(0, score_bonus[2])
            main_surface.blit(score_bonus[0], score_bonus[1])
            if score_bonus[1].top >= height + score_bonus[2]:
                score_bonuses.pop(score_bonuses.index(score_bonus))
            if player_rect.colliderect(score_bonus[1]):
                score_bonuses.pop(score_bonuses.index(score_bonus))
                score = score + 100
                enemy_min_speed += 1
                enemy_max_speed += 2
                enemy_min_size += 5
                enemy_max_size += 5
                bg_speed += 0.5

        for speed_bonus in speed_bonuses:
            speed_bonus[1] = speed_bonus[1].move(0, speed_bonus[2])
            main_surface.blit(speed_bonus[0], speed_bonus[1])
            if speed_bonus[1].top >= height + speed_bonus[2]:
                speed_bonuses.pop(speed_bonuses.index(speed_bonus))
            if player_rect.colliderect(speed_bonus[1]):
                speed_bonuses.pop(speed_bonuses.index(speed_bonus))
                player_speed += 1

        for i in range (0, len(enemies)):
            if len(score_bonuses) > 0 and enemies[i][1].colliderect(score_bonuses[0][1]):
                score_bonuses.pop(score_bonuses.index(score_bonus))
            if len(life_bonuses) > 0 and enemies[i][1].colliderect(life_bonuses[0][1]):
                life_bonuses.pop(life_bonuses.index(life_bonus))
            if len(speed_bonuses) > 0 and enemies[i][1].colliderect(speed_bonuses[0][1]):
                speed_bonuses.pop(speed_bonuses.index(speed_bonus))

        if pressed_keys[K_DOWN] and player_rect.bottom <= height - player_speed:
            player_rect = player_rect.move(0, player_speed)
        if pressed_keys[K_UP] and player_rect.top >= 0 + player_speed:
            player_rect = player_rect.move(0, -player_speed)
        if pressed_keys[K_LEFT] and player_rect.left >= 0 + player_speed:
            player_rect = player_rect.move(-player_speed, 0)
        if pressed_keys[K_RIGHT] and player_rect.right <= width - player_speed:
            player_rect = player_rect.move(player_speed, 0)
        if pressed_keys[K_p]: 
            is_pause = True

    pg.display.flip()

print(len(enemies), len(life_bonuses), len(score_bonuses), len(speed_bonuses))
print ('The end...')
