import os.path
import pygame
import random

pygame.init()


fuel_image =pygame.image.load("larvae.png")
fuel_sound = pygame.mixer.Sound("sound/effects/glassbell.wav")

class food():
    icon = fuel_image
    #icon_mask = pygame.mask.from_surface(icon)
    def __init__(self, x, y, screen_width, screen_height):
        self.x = x
        self.y = y
        self.scrn_width = screen_width
        self.scrn_height = screen_height
        self.width = self.icon.get_width()
        self.height = self.icon.get_height()

    def draw(self, screen):
        screen.blit(self.icon, (self.x, self.y, self.width, self.height))
        #pygame.draw.rect(screen, 'green', self.hitbox, 2)

    def collided(self, screen):
        self.x = random.randint(0,(int(self.scrn_width) - 9 - self.width))
        self.y = random.randint(0,(int(self.scrn_height-9 - self.height)))
        pygame.mixer.Sound.play(fuel_sound)

        font = pygame.font.SysFont('elephant',24, True, False)
        text = font.render("+Fuel", 1,'green')
        screen.blit(text, ((self.scrn_width // 2) - (text.get_width() // 2), (720 * 0.9) / 2))

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


class health():
    def __init__(self, x, y, width, height, fuel, max_fuel, screen_width, screen_height):
        self.contents = None
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fuel = fuel
        self.max_fuel = max_fuel
        self.score = 0

        self.scrn_width = screen_width
        self.scrn_height = screen_height

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
            screen.blit(text, (20, int(self.scrn_height-40)))
        else:
            font_low = pygame.font.SysFont('elephant', 20)
            text = font_low.render(f"fuel tank: {round((self.fuel / self.max_fuel) * 100, 2)} % !!!", 1, 'red')
            screen.blit(text, (20, int(self.scrn_height - 40)))



        font_score = pygame.font.SysFont('elephant', 20)
        text = font_score.render(f"Score: {self.score} ", 1, 'green')
        screen.blit(text, (int(self.scrn_width - 60)- text.get_width()/2, 40))

        font_HighScore = pygame.font.SysFont('times new roman', 15)
        text_HighScore = font_HighScore.render(f"High Score: {self.contents} ", 1, 'white')
        screen.blit(text_HighScore, (int(self.scrn_width - 60) - text_HighScore.get_width() / 2, text.get_height() +50))

        #
    def empty(self, screen):
        font1 = pygame.font.SysFont('elephant', 30, True, True)
        text = font1.render("NO FUEL YOU ARE LOSSSSSSEEEE!!!1", 1, 'red')
        screen.blit(text, ((self.scrn_width // 2) - (text.get_width() // 2), (720 * 0.9) / 2))
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




class Enemy:
    img = pygame.image.load('bug.png')
    enemies = [pygame.image.load('bug.png')]
    enemies_l = [pygame.transform.flip(img,False, True)]
    bugs = []

    def __init__(self, screen_width, screen_height):


        self.enemies_available = False
        self.screen_width = screen_width
        self.x = random.randint(0,int(screen_width-67))
        self.x2 = random.randint(0, int(screen_width - 67))
        self.y = -300
        self.vel = 5
        self.difficulty = 0
        self.facing = 1
        self.scrn_width = screen_width
        self.scrn_height = screen_height

    def draw(self, screen):
        if self.enemies_available:
            if self.vel > 0:

                self.move_down()


                screen.blit(self.enemies[0],( self.x, self.y))
                screen.blit(self.enemies[0], (self.x2, self.y))
                screen.blit(self.enemies[0], (abs(self.x2 -self.x), self.y))

            if screen.get_height() < self.y < screen.get_height()+20:
                self.x = random.randint(0, int(self.screen_width - 67))

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
            if  self.y < self.scrn_height+310:
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
