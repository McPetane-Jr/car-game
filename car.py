#==========Imports================================================
#Car script:

import pygame
import math
from utils import blit_rotate_center, scale_image

pygame.init()

#=========Vehicle assets===================================================
vehicle = pygame.image.load('images/car/LadyBugCar.png')
Moving_vehicle = pygame.image.load('images/car/LadyBugCarMoving.png')
Reversing_vehicle = pygame.image.load('images/car/LadyBugCarReversing.png')
Shield = scale_image(pygame.image.load('images/props/Shild.png'), 1.5)

class car():

    IMG_static = vehicle
    IMG_fwd = Moving_vehicle
    IMG_bwd = Reversing_vehicle

    def __init__(self, rotation_vel, x, y):
        self.img_static = self.IMG_static
        self.img = self.IMG_fwd
        self.img_reversing = self.IMG_bwd
        self.vel = 0
        self.max_vel = 8          # fixed: was 800
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.acceleration = 0.2   # fixed: was 2
        self.x = x
        self.y = y
        self.moving_fwd = False
        self.moving_bwd = False
        self.bomb_drop = False
        self.x_pos = self.x
        self.y_pos = self.y
        self.shield_active = False

        # Pre-computed masks — faster than rebuilding every frame
        self.mask_fwd = pygame.mask.from_surface(self.IMG_fwd)
        self.mask_bwd = pygame.mask.from_surface(self.IMG_bwd)
        self.mask_static = pygame.mask.from_surface(self.IMG_static)



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
            car_mask = self.mask_fwd
        elif self.moving_bwd:
            car_mask = self.mask_bwd
        else:
            car_mask = self.mask_static

        offset = (int(self.x - x), int(self.y - y))
        return mask.overlap(car_mask, offset)
    
    # def hit(self, mask, x, y):

    #     if self.moving_fwd:
    #         car_mask = pygame.mask.from_surface(self.IMG_fwd)
    #         offset = (int(self.x - x), int(self.y - y))
    #         poi = mask.overlap(car_mask , offset)

    #         return poi

    #     if self.moving_bwd:
    #         car_mask = pygame.mask.from_surface(self.IMG_bwd)
    #         offset = (int(self.x - x), int(self.y - y))
    #         poi = mask.overlap(car_mask , offset)
    #         return poi

    #     if not self.moving_bwd or self.moving_bwd:
    #         car_mask = pygame.mask.from_surface(self.IMG_static)
    #         offset = (int(self.x - x), int(self.y - y))
    #         poi = mask.overlap(car_mask , offset)
    #         return poi

    #     if self.moving_fwd:
    #         car_mask = pygame.mask.from_surface(self.IMG_fwd)
    #         offset = (int(self.x - x), int(self.y - y))
    #         bad_poi = mask.overlap(car_mask, offset)
    #         return bad_poi

    def x(self):
        p = self.x
        pass
    def y(self):
        q = self.y
        return self.q
#================================================================================


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
# import pygame
# import math
# from utils import blit_rotate_center, scale_image

# pygame.init()

vehicle = pygame.image.load('images/car/LadyBugCar.png')
Moving_vehicle = pygame.image.load('images/car/LadyBugCarMoving.png')
Reversing_vehicle = pygame.image.load('images/car/LadyBugCarReversing.png')
Shield = scale_image(pygame.image.load('images/props/Shild.png'), 1.5)


class car():
    IMG_static = vehicle
    IMG_fwd = Moving_vehicle
    IMG_bwd = Reversing_vehicle

    
    def rotation(self, left=False, right=True):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, screen):
        if self.moving_fwd:
            blit_rotate_center(screen, self.img, (self.x, self.y), self.angle)
        elif self.moving_bwd:
            blit_rotate_center(screen, self.img_reversing, (self.x, self.y), self.angle)
        else:
            blit_rotate_center(screen, self.img_static, (self.x, self.y), self.angle)

        if self.shield_active:
            screen.blit(Shield, (self.x, self.y))

    def move_fwd(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move1()

    def reverse(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move1()

    def move1(self):
        rad = math.radians(self.angle)
        self.y -= math.cos(rad) * self.vel
        self.x -= math.sin(rad) * self.vel

    def slow_down(self):
        self.vel = max(self.vel - self.acceleration * 0.8, 0)
        self.move1()

    