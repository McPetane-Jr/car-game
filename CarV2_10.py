#Main script:



import math
import random


from car import car, Bombs
from entities import food, health, Enemy, fuel_image
from game_info import Game_info

import pygame
from utils import blit_rotate_center, scale_image

pygame.init()

#Defining the screen width and height

small_scrn_width, small_scrn_height = 1280 * 0.9, 720 * 0.9
screen_width, screen_height = small_scrn_width, small_scrn_height


#BACKGROUND

bg = pygame.image.load("bg.jpg")



#Setting up the screen and clock
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("CAR")
clock = pygame.time.Clock()


#MUSIC

pygame.mixer.music.load('Here Comes a Thought - Steven Universe Karaoke [Official Instrumental](MP3_160K).mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # Play the music indefinitely
mute = False

     

#Defining the game objects

centipedes = Enemy(screen_width, screen_height)
game = Game_info()
cyberBug = car(14,20,350)
bomb = Bombs(4, 20, 350)
fuel_icon = food(random.randint(5, 1000 - fuel_image.get_width() - 100),
                 random.randint(0, 550 - fuel_image.get_height() - 50), screen_width, screen_height)
hp = health(20, 20, 140, 20, 140, 140, screen_width, screen_height)



#Defining the animate function:

def animate():
    screen.blit(bg, (0,0))
    fuel_icon.draw(screen)
    cyberBug.draw(screen)
    hp.draw(screen)
    centipedes.draw(screen)
    #game.power_up(screen)
    bomb.draw(screen, 20, 45)
    pygame.display.update()





#Defining the buttons function:

def buttons():
    
    moving = False

    if keys[pygame.K_v]:
        cyberBug.shield_active = True     # V-> shield

    if keys[pygame.K_f]:
        bomb.detonate()
    else:
        bomb.F_down = False

    if keys[pygame.K_g]:
        if bomb.count > 0 and not bomb.exploded:
            bomb.solid = False
            bomb.exploded = True



    if keys[pygame.K_SPACE]:
        cyberBug.max_vel = 20
        cyberBug.rotation_vel = 11.5
        cyberBug.acceleration = 2
        bomb.x, bomb.y = cyberBug.x, cyberBug.y
    else:
        cyberBug.max_vel = 8
        cyberBug.rotation_vel = 4
        cyberBug.acceleration = 0.2
        bomb.x, bomb.y = cyberBug.x, cyberBug.y

    if keys[pygame.K_w] and hp.fuel > 0:
        cyberBug.moving_fwd = True
        moving = True
        cyberBug.move_fwd()
        bomb.x, bomb.y = cyberBug.x, cyberBug.y

    if keys[pygame.K_s]:
        cyberBug.moving_bwd = True
        moving = True
        cyberBug.reverse()
        bomb.x, bomb.y = cyberBug.x, cyberBug.y

    #if keys[pygame.K_d]:
    if keys[pygame.K_RIGHT]:
        cyberBug.rotation(right=True)
        cyberBug.rotation(left=False)
        bomb.x, bomb.y = cyberBug.x, cyberBug.y

    #if keys[pygame.K_a]:
    if keys[pygame.K_LEFT]:
        cyberBug.rotation(right=False)
        cyberBug.rotation(left=True)
        bomb.x, bomb.y = cyberBug.x, cyberBug.y

    if not moving:
        cyberBug.moving_fwd = False
        cyberBug.moving_bwd = False
        cyberBug.slow_down()
        bomb.x, bomb.y = cyberBug.x, cyberBug.y

    if moving:

        if hp.fuel > 0:
            hp.fuel -= 0.247

    if hp.fuel <= 0:
        hp.empty(screen)

    




#====================Defining the collision control function================================================
def collision_cntrl():

    if cyberBug.hit(fuel_icon.col(), fuel_icon.x, fuel_icon.y) is not None:
        hp.fuel += 12.5
        game.progress += 1
        hp.score += 1
        fuel_icon.collided(screen)




        print("yay")

    if cyberBug.hit(centipedes.enemy_mask(), centipedes.x, centipedes.y) is not None:
        hp.fuel -= 2.125
        rad = math.radians(cyberBug.angle)
        cyberBug.vel = -((8 * math.sin(rad)) ** 2 + (8 * math.cos(rad)) ** 2) ** (1 / 2)
        print("it worked")

    if cyberBug.hit(centipedes.enemy_mask(), abs(centipedes.x2 - centipedes.x), centipedes.y) is not None:
        hp.fuel -= 2.125
        rad = math.radians(cyberBug.angle)
        cyberBug.vel = -((8 * math.sin(rad)) ** 2 + (8 * math.cos(rad)) ** 2) ** (1 / 2)
        print("it worked")

    if cyberBug.hit(centipedes.enemy_mask(), centipedes.x2, centipedes.y) is not None:
        hp.fuel -= 2.125
        rad = math.radians(cyberBug.angle)
        cyberBug.vel = -((8 * math.sin(rad)) ** 2 + (8 * math.cos(rad)) ** 2) ** (1 / 2)
        print("it worked")



#====================Defining the main game loop================================================
start_game = True



while start_game:
    clock.tick(32)




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit("Bitch, I didn't want you playin' me anyway! \n HOO")

    keys = pygame.key.get_pressed()


    if not mute:
        pygame.mixer.music.play(-1)

    else:
        pygame.mixer.stop()


    buttons()
    collision_cntrl()
    hp.save_score()


    if game.progress//5  == game.lvl:

        game.next_lvl()
        centipedes.vel += game.lvl

    if game.lvl > 1:
        centipedes.enemies_available = True


    screen.fill('black')
    animate()


