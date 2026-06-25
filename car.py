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

    def __init__(self, rotation_vel, x, y, screen_width, screen_height):

        #IMAGE DEFINITION:
        self.img_static = self.IMG_static
        self.img = self.IMG_fwd
        self.img_reversing = self.IMG_bwd

        #DIMENSIONS:
        self.scrn_width = screen_width
        self.scrn_height = screen_height
        self.car_w = self.IMG_static.get_width()
        self.car_h = self.IMG_static.get_height()

        #velocity:
        self.vel = 0
        self.max_vel = 8
        self.rotation_vel = rotation_vel

        #POSITION:
        self.angle = 0
        self.acceleration = 0.2   # fixed: was 2
        self.x = x
        self.y = y

        #Booleans:
        self.moving_fwd = False
        self.moving_bwd = False
        self.bomb_drop = False
        
        self.shield_active = False

        # Pre-computed masks — faster than rebuilding every frame
        self.mask_fwd = pygame.mask.from_surface(self.IMG_fwd)
        self.mask_bwd = pygame.mask.from_surface(self.IMG_bwd)
        self.mask_static = pygame.mask.from_surface(self.IMG_static)

    def wrap(self):
        w, h = self.car_w, self.car_h

        if self.x > self.scrn_width + w * 0.5:
            self.x = -w * 0.5          # exit right → enter left
        elif self.x < -w * 1.5:
            self.x = self.scrn_width - w * 0.5  # exit left → enter right

        if self.y > self.scrn_height + h * 0.5:
            self.y = -h * 0.5          # exit bottom → enter top
        elif self.y < -h * 1.5:
            self.y = self.scrn_height - h * 0.5  # exit top → enter bottom

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

        self.vel = min((self.vel + self.acceleration), self.max_vel)
        #this makes sue we can't keep accelerating after reaching max vel
        
        
        self.move1()

    def reverse(self):

        self.vel = max((self.vel - self.acceleration),
                       -self.max_vel/2)  
        # this makes sue we can't keep accelerating after reaching max vel
        
        
        self.move1()

    def move1(self):
        rad = math.radians(self.angle)
        fwd = math.cos(rad) * self.vel
        horizontal = math.sin(rad) * self.vel

        self.y -= fwd
        self.x -= horizontal

        self.wrap()  # check boundary every time car moves



    def move2(self):
        rad = math.radians(self.angle)
        fwd = math.cos(rad) * self.vel
        horizontal = math.sin(rad) * self.vel

        self.y += fwd
        self.x -= horizontal

    def slow_down(self):
        if self.vel > 0:
            self.vel = max(self.vel - self.acceleration * 0.8, 0)
        elif self.vel < 0:
            self.vel = min(self.vel + self.acceleration * 0.8, 0)  # decelerates back to 0
        self.move1()
    
    def hit(self, mask, x, y):
        if self.moving_fwd:
            car_mask = self.mask_fwd
        elif self.moving_bwd:
            car_mask = self.mask_bwd
        else:
            car_mask = self.mask_static

        offset = (int(self.x - x), int(self.y - y))
        return mask.overlap(car_mask, offset)
    
#================================================================================


class Bombs(car):
    Explosions = [pygame.image.load('images/props/E00.png'),
                  pygame.image.load('images/props/E11.png'),
                  pygame.image.load('images/props/E2.png'),
                  pygame.image.load('images/props/E3.png'),
                  pygame.image.load('images/props/E4.png'),
    ]

    Bomb = pygame.image.load('images/props/Bomb.png')

    def __init__(self, rotation_vel, x, y, screen_width, screen_height):
        super().__init__(rotation_vel, x, y, screen_width, screen_height)

        self.bombs = []
        self.F_down = False
        self.exploded = False
        self.solid = True
        self.speed = 0.5
        self.exp_index = 0
        self.count = 0

        self.small_bomb = pygame.transform.scale(self.Bomb, (20, 20))

    def detonate(self):
    
        if not self.F_down and len(self.bombs) < 1:
            self.bombs.append((self.x, self.y))
            self.F_down = True
            self.count += 1
            self.solid = True
            self.exploded = False

    def _reset(self): # One single place that handles all cleanup
        self.exploded = False
        self.count = 0
        self.exp_index = 0
        self.bombs.clear()

    def draw(self, screen, screen_x, screen_y):

        
        if not self.bombs:   # "if the bombs list is empty exit func/methd"
            
            screen.blit(self.small_bomb, (screen_x, screen_y))  # sits just under the health bar
            return
        
        self.explode()

        for bomb_x, bomb_y in self.bombs:
            if self.solid and not self.exploded:
                screen.blit(self.Bomb, (bomb_x, bomb_y))

            elif self.exploded:
                current = int(self.exp_index)
                if current < len(self.Explosions):   # fixed: was <=
                    screen.blit(self.Explosions[current], (bomb_x, bomb_y))

        # Cleanup happens AFTER the loop, never inside it
        if not self.solid and self.exploded and int(self.exp_index) >= len(self.Explosions):
            self._reset()


    def explode(self):
        if self.exploded:
            self.exp_index += self.speed
#========================================================================================
