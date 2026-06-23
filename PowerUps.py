import pygame
pygame.init()
from CarV2_10 import car

class Bombs(car):
    Bomb = pygame.image.load('/Games/car game/images/props/Bomb.png')
    def __init__(self, rotation_vel, x, y):
        super().__init__(rotation_vel, x, y)

        self.bombs = []
        self.F_down = False

    def detonate(self):
        if not self.F_down:
            self.bombs.append((self.x, self.y))
            self.F_down = True

    def draw(self, screen):
        for bomb_x, bomb_y in self.bombs:
            screen.blit(self.Bomb, (bomb_x, bomb_y))