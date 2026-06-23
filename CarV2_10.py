import os.path
#from cgitb import small
from itertools import count
from math import radians
from pickle import GLOBAL

from PIL.ImageChops import offset
#from pygame.time import get_ticks
from urllib3.filepost import writer

#import timer
from utils import blit_rotate_center, scale_image
import pygame
import math
import random
#from PowerUps import *
#from timer import Timer


pygame.init()

#====================Defining the screen width and height
small_scrn_width, small_scrn_height = 1280 * 0.9, 720 * 0.9
screen_width, screen_height = small_scrn_width, small_scrn_height
#====================================================================================

#====================Defining assets for the game===========================================
bg = pygame.image.load("bg.jpg")
vehicle = pygame.image.load('images/car/LadyBugCar.png')
Moving_vehicle = pygame.image.load('images/car/LadyBugCarMoving.png')
Reversing_vehicle = pygame.image.load('images/car/LadyBugCarReversing.png')
Shield = scale_image(pygame.image.load('images/props/Shild.png'), 1.5)
fuel_icon =pygame.image.load("larvae.png")
#=====================================================================================

#====================Setting up the screen and clock===========================================
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("CAR")
clock = pygame.time.Clock()
song = pygame.mixer.music.load('Here Comes a Thought - Steven Universe Karaoke [Official Instrumental](MP3_160K).mp3')
mute = False
#=======================================================================================


#====================Defining the sound effects================================================
fuel_sound = pygame.mixer.Sound("sound/effects/glassbell.wav")

#=======================================================================================


#====================Defining the car class================================================
class car():

    IMG_static = vehicle
    IMG_fwd = Moving_vehicle
    IMG_bwd = Reversing_vehicle

    def __init__(self, rotation_vel, x, y):
        self.img_static = self.IMG_static
        self.img = self.IMG_fwd
        self.img_reversing = self.IMG_bwd
        self.vel = 0
        self.max_vel = 8
        self.rotation_vel = rotation_vel
        self.angle = 0 #This is our starting angle
        self.acceleration = 0.2
        self.x = x
        self.y = y
        self.moving_fwd = False
        self.moving_bwd = False
        self.bomb_drop = False
        self.x_pos = self.x
        self.y_pos = self.y


        self.shield_active = False


    def rotation(self, left = False, right = True):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, screen):
        if self.moving_fwd:
            blit_rotate_center(screen, self.img, (self.x, self.y), self.angle)
        if self.moving_bwd:
            blit_rotate_center(screen, self.img_reversing, (self.x, self.y), self.angle)
        if not self.moving_bwd or self.moving_fwd:
            blit_rotate_center(screen, self.img_static, (self.x, self.y), self.angle)

        if self.shield_active:
            screen.blit(Shield, (self.x, self.y))

        #print(self.x)





    def move_fwd(self):

        self.vel = min((self.vel + self.acceleration), self.max_vel)#this makes sue we can't keep accelerating after reaching max vel
        self.move1()

    def reverse(self):

        self.vel = max((self.vel - self.acceleration),
                       -self.max_vel/2)  # this makes sue we can't keep accelerating after reaching max vel
        self.move1()

    def move1(self):
        rad = math.radians(self.angle)
        fwd = math.cos(rad) * self.vel
        horizontal = math.sin(rad) * self.vel

        self.y -= fwd
        self.x -= horizontal


    def move2(self):
        rad = math.radians(self.angle)
        fwd = math.cos(rad) * self.vel
        horizontal = math.sin(rad) * self.vel

        self.y += fwd
        self.x -= horizontal

    def slow_down(self):
        self.vel = max(self.vel-self.acceleration*0.8, 0) #makes so we reduce the velocity till we get to 0
        self.move1()#Let's go call the bad boi out in the loop

    def hit(self, mask, x, y):

        if self.moving_fwd:
            car_mask = pygame.mask.from_surface(self.IMG_fwd)
            offset = (int(self.x - x), int(self.y - y))
            poi = mask.overlap(car_mask , offset)

            return poi

        if self.moving_bwd:
            car_mask = pygame.mask.from_surface(self.IMG_bwd)
            offset = (int(self.x - x), int(self.y - y))
            poi = mask.overlap(car_mask , offset)
            return poi

        if not self.moving_bwd or self.moving_bwd:
            car_mask = pygame.mask.from_surface(self.IMG_static)
            offset = (int(self.x - x), int(self.y - y))
            poi = mask.overlap(car_mask , offset)
            return poi

        if self.moving_fwd:
            car_mask = pygame.mask.from_surface(self.IMG_fwd)
            offset = (int(self.x - x), int(self.y - y))
            bad_poi = mask.overlap(car_mask, offset)
            return bad_poi

    def x(self):
        p = self.x
        pass
    def y(self):
        q = self.y
        return self.q
#================================================================================


#====================Defining the Bombs class================================================
class Bombs(car):
    Explosions = [pygame.image.load('images/props/E00.png'),
                  pygame.image.load('images/props/E11.png'),
                  pygame.image.load('images/props/E2.png'),
                  pygame.image.load('images/props/E3.png'),
                  pygame.image.load('images/props/E4.png'),
    ]
    Bomb = pygame.image.load('images/props/Bomb.png')
    def __init__(self, rotation_vel, x, y):
        super().__init__(rotation_vel, x, y)

        self.bombs = []
        self.F_down = False
        self.exploded = False
        self.solid = True
        self.speed = 0.005
        self.exp_index = 0
        self.count = 0

    def detonate(self):
        if not self.F_down:
            if len(self.bombs) < 1:
                self.bombs.append((self.x, self.y))
                self.F_down = True
                self.count+=1
                self.solid = True
                self.exploded = False


    def draw(self, screen):
        self.explode()
        for bomb_x, bomb_y in self.bombs:
            if self.solid and not self.exploded:
                screen.blit(self.Bomb, (bomb_x, bomb_y))
            elif self.exploded and self.exp_index <= len(self.Explosions):
                current = int(self.exp_index)
                screen.blit(self.Explosions[current], (bomb_x, bomb_y))

            if not self.solid and self.exploded:

                self.exploded = False
                self.count = 0
                self.bombs.clear()


    def explode(self):
        self.exp_index += self.speed
        if self.exp_index >= len(self.Explosions):
            self.bombs.clear()
            self.exp_index = 0
#========================================================================================




#====================Defining the food class================================================
class food():
    icon = fuel_icon
    #icon_mask = pygame.mask.from_surface(icon)
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = self.icon.get_width()
        self.height = self.icon.get_height()

    def draw(self):
        screen.blit(self.icon, (self.x, self.y, self.width, self.height))
        #pygame.draw.rect(screen, 'green', self.hitbox, 2)

    def collided(self):
        self.x = random.randint(0,(int(small_scrn_width) - 9 - self.width))
        self.y = random.randint(0,(int(small_scrn_height-9 - self.height)))
        pygame.mixer.Sound.play(fuel_sound)

        font = pygame.font.SysFont('elephant',24, True, False)
        text = font.render("+Fuel", 1,'green')
        screen.blit(text, ((small_scrn_width // 2) - (text.get_width() // 2), (720 * 0.9) / 2))

        pygame.display.update()
        i=0
        while i < 300000:
            i+=1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()



    def col(self):

        return pygame.mask.from_surface(self.icon)

#======================================================================================


#====================Defining the health class================================================
class health():
    def __init__(self, x, y, width, height, fuel, max_fuel):
        self.contents = None
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fuel = fuel
        self.max_fuel = max_fuel
        self.score = 0

    def save_score(self):
        file_path = "images/high score/currentHighScore.txt"
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                self.contents= file.read()
                #print(contents)
                if  self.score > int(self.contents):
                    with open(file_path, "w") as file:
                        file.write(str(self.score))

        else:
            with open(file_path, "w") as file:
                self.contents = 0
                file.write(str(0))

    def draw(self, screen):

        pygame.draw.rect(screen, 'red', (20, 20, 140, 20))
        pygame.draw.rect(screen, "green", (20, 20, self.fuel * (self.fuel/self.max_fuel), 20))
        if (self.fuel/self.max_fuel)*100 > 30:
            font = pygame.font.SysFont('elephant', 20)
            text = font.render(f"fuel tank: {round((self.fuel/self.max_fuel)*100, 2)} %", 1, 'green')
            screen.blit(text, (20, int(screen_height-40)))
        else:
            font_low = pygame.font.SysFont('elephant', 20)
            text = font_low.render(f"fuel tank: {round((self.fuel / self.max_fuel) * 100, 2)} % !!!", 1, 'red')
            screen.blit(text, (20, int(screen_height - 40)))



        font_score = pygame.font.SysFont('elephant', 20)
        text = font_score.render(f"Score: {self.score} ", 1, 'green')
        screen.blit(text, (int(screen_width - 60)- text.get_width()/2, 40))

        font_HighScore = pygame.font.SysFont('times new roman', 15)
        text_HighScore = font_HighScore.render(f"High Score: {self.contents} ", 1, 'white')
        screen.blit(text_HighScore, (int(screen_width - 60) - text_HighScore.get_width() / 2, text.get_height() +50))

        #
    def empty(self):
        font1 = pygame.font.SysFont('elephant', 30, True, True)
        text = font1.render("NO FUEL YOU ARE LOSSSSSSEEEE!!!1", 1, 'red')
        screen.blit(text, ((small_scrn_width // 2) - (text.get_width() // 2), (720 * 0.9) / 2))
        pygame.display.update()
        i = 0
        while i < 20000000:
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    exit("Better luck next time!!!!")
                if event.type == pygame.QUIT:
                    exit("Loseeeerrrrr")

#======================================================================================


#====================Defining the Game_info class================================================
#This class will keep track of the wins, losses and levels
class Game_info:
    levels = 3
    def __init__(self, lvl = 1):
        self.lvl = lvl
        self.progress = 0
        self.active_power_up = False
        self.start_time = 0
        self.key = False
        self.count = 0
        self.timer_worked = False


    def next_lvl(self):
        self.lvl += 1
        print(f"Current Game level: {self.lvl}")
        return self.lvl

    def game_over(self):
        return self.lvl > self.levels

        #pygame.draw.rect(screen, 'red', (200, 300, 40, 40))


class Enemy:
    img = pygame.image.load('bug.png')
    enemies = [pygame.image.load('bug.png')]
    enemies_l = [pygame.transform.flip(img,False, True)]
    bugs = []

    def __init__(self):


        self.enemies_available = False
        self.x = random.randint(0,int(screen_width-67))
        self.x2 = random.randint(0, int(screen_width - 67))
        self.y = -300
        self.vel = 5
        self.difficulty = 0
        self.facing = 1

    def draw(self, screen):
        if self.enemies_available:
            if self.vel > 0:

                self.move_down()


                screen.blit(self.enemies[0],( self.x, self.y))
                screen.blit(self.enemies[0], (self.x2, self.y))
                screen.blit(self.enemies[0], (abs(self.x2 -self.x), self.y))

            if screen.get_height() < self.y < screen.get_height()+20:
                self.x = random.randint(0, int(screen_width - 67))

            if self.vel <= 0:
                self.move_up()
                screen.blit(self.enemies_l[0], (self.x, self.y))
                screen.blit(self.enemies_l[0], (self.x2, self.y))
                screen.blit(self.enemies_l[0], (abs(self.x2 - self.x), self.y))

    def enemy_mask(self):
        if self.vel > 0:
            return pygame.mask.from_surface(self.enemies[0])
        else:
            return pygame.mask.from_surface(self.enemies_l[0])

    def move_down(self):
            #self.facing = 1
            if  self.y < screen.get_height()+310:
                self.y += self.vel
            else:
                self.vel *= -1
    def move_up(self):

            if self.y > -300:

                self.y += self.vel
            else:
                self.vel *= -1

    #def bug(self):
 #============================================================================
        

#======================Defining the game objects================================================
centipedes = Enemy()

duration = True
game = Game_info()

kar = car(4,20,350)
bomb = Bombs(4, 20, 350)


fuel_icon = food(random.randint(5, 1000 - fuel_icon.get_width() - 100),
                 random.randint(0, 550 - fuel_icon.get_height() - 50))

hp = health(20, 20, 140, 20, 140, 140)

#================================================================


#====================Defining the animate function================================================
def animate():
    screen.blit(bg, (0,0))
    fuel_icon.draw()
    kar.draw(screen)
    hp.draw(screen)
    centipedes.draw(screen)
    #game.power_up(screen)
    bomb.draw(screen)
    pygame.display.update()





#====================Defining the buttons function================================================
def buttons():
    global mute
    moving = False
    # reversing = False
    if keys[pygame.K_v]:
        kar.shield_active = True

    if keys[pygame.K_f]:
        bomb.detonate()
    else:
        bomb.F_down = False

    if keys[pygame.K_g]:
        if bomb.count > 0 and not bomb.exploded:
            bomb.solid = False
            bomb.exploded = True



    if keys[pygame.K_SPACE]:
        kar.max_vel = 15
        kar.rotation_vel = 8
        kar.acceleration = 2
        bomb.x, bomb.y = kar.x, kar.y
    else:
        kar.max_vel = 8
        kar.rotation_vel = 4
        kar.acceleration = 0.2
        bomb.x, bomb.y = kar.x, kar.y

    if keys[pygame.K_w] and hp.fuel > 0:
        kar.moving_fwd = True
        moving = True
        kar.move_fwd()
        bomb.x, bomb.y = kar.x, kar.y

    if keys[pygame.K_s]:
        kar.moving_bwd = True
        moving = True
        kar.reverse()
        bomb.x, bomb.y = kar.x, kar.y

    #if keys[pygame.K_d]:
    if keys[pygame.K_RIGHT]:
        kar.rotation(right=True)
        kar.rotation(left=False)
        bomb.x, bomb.y = kar.x, kar.y

    #if keys[pygame.K_a]:
    if keys[pygame.K_LEFT]:
        kar.rotation(right=False)
        kar.rotation(left=True)
        bomb.x, bomb.y = kar.x, kar.y

    if not moving:
        kar.moving_fwd = False
        kar.moving_bwd = False
        kar.slow_down()
        bomb.x, bomb.y = kar.x, kar.y

    if moving:

        if hp.fuel > 0:
            hp.fuel -= 0.247

    if hp.fuel <= 0:
        hp.empty()

    if keys[pygame.K_m]:
        if not mute:
            mute = True
        else:
            mute = False




#====================Defining the collision control function================================================
def collision_cntrl():

    if kar.hit(fuel_icon.col(), fuel_icon.x, fuel_icon.y) is not None:
        hp.fuel += 12.5
        game.progress += 1
        hp.score += 1
        fuel_icon.collided()




        print("yay")

    if kar.hit(centipedes.enemy_mask(), centipedes.x, centipedes.y) is not None:
        hp.fuel -= 2.125
        rad = math.radians(kar.angle)
        kar.vel = -((8 * math.sin(rad)) ** 2 + (8 * math.cos(rad)) ** 2) ** (1 / 2)
        print("it worked")

    if kar.hit(centipedes.enemy_mask(), abs(centipedes.x2 - centipedes.x), centipedes.y) is not None:
        hp.fuel -= 2.125
        rad = math.radians(kar.angle)
        kar.vel = -((8 * math.sin(rad)) ** 2 + (8 * math.cos(rad)) ** 2) ** (1 / 2)
        print("it worked")

    if kar.hit(centipedes.enemy_mask(), centipedes.x2, centipedes.y) is not None:
        hp.fuel -= 2.125
        rad = math.radians(kar.angle)
        kar.vel = -((8 * math.sin(rad)) ** 2 + (8 * math.cos(rad)) ** 2) ** (1 / 2)
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


