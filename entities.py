#Entities script:
import os.path
import pygame
import random

pygame.init()


fuel_image =pygame.image.load("larvae.png")
fuel_sound = pygame.mixer.Sound("sound/effects/glassbell.wav")

class food():
    icon = fuel_image
    icon_mask = pygame.mask.from_surface(icon)

    def __init__(self, x, y, screen_width, screen_height):
        self.x = x
        self.y = y
        self.scrn_width = screen_width
        self.scrn_height = screen_height
        self.width = self.icon.get_width()
        self.height = self.icon.get_height()

        self.font = pygame.font.SysFont('elephant', 24, True, False)
        self.text = self.font.render("+Fuel", 1, 'green')
        self.show_fuel_text_until = 0  # 0 means "don't show

    def draw(self, screen):
        screen.blit(self.icon, (self.x, self.y, self.width, self.height))
        #pygame.draw.rect(screen, 'green', self.hitbox, 2)

        if pygame.time.get_ticks() < self.show_fuel_text_until:
            
            
            screen.blit(self.text, (
                (self.scrn_width // 2) - (self.text.get_width() // 2),
                self.scrn_height // 2
            ))

    def collided(self):
        self.x = random.randint(0,(int(self.scrn_width) - 9 - self.width))
        self.y = random.randint(0,(int(self.scrn_height-9 - self.height)))
        pygame.mixer.Sound.play(fuel_sound)

        self.show_fuel_text_until = pygame.time.get_ticks() + 1000  # show for 1 second



    def col(self):

        return self.icon_mask


class health():
    # Fonts pre-created once at class level
    font_fuel = pygame.font.SysFont('elephant', 20)
    font_score = pygame.font.SysFont('elephant', 20)
    font_hs = pygame.font.SysFont('times new roman', 15)
    font_empty = pygame.font.SysFont('elephant', 30, True, True)

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

        fuel_pct = (self.fuel / self.max_fuel) * 100
        color = 'green' if fuel_pct > 30 else 'red'
        suffix = '' if fuel_pct > 30 else ' !!!'
        text = self.font_fuel.render(
            f"fuel tank: {round(fuel_pct, 2)} %{suffix}", 1, color)
        screen.blit(text, (20, int(self.scrn_height - 40)))



        text_score = self.font_score.render(f"Score: {self.score}", 1, 'green')
        screen.blit(text_score,
                    (int(self.scrn_width - 60) - text_score.get_width() / 2, 40))

        text_hs = self.font_hs.render(f"High Score: {self.contents}", 1, 'white')
        screen.blit(text_hs, (
            int(self.scrn_width - 60) - text_hs.get_width() / 2,
            text_score.get_height() + 50
        ))



        
    def empty(self, screen):
        font1 = pygame.font.SysFont('elephant', 30, True, True)
        text = font1.render("NO FUEL YOU ARE LOSSSSSSEEEE!!!", 1, 'red')
        screen.blit(text, ((self.scrn_width // 2) - (text.get_width() // 2), (720 * 0.9) / 2))
        pygame.display.update()
        

#======================================================================================




class Enemy:
    
    enemies = [pygame.image.load('bug.png')]
    enemies_l = [pygame.transform.flip(enemies[0], False, True)]
    enemy_mask_fwd = pygame.mask.from_surface(enemies[0])  # pre-computed
    enemy_mask_bwd = pygame.mask.from_surface(enemies_l[0])
    

    def __init__(self, screen_width, screen_height, current_lvl):


        self.enemies_available = False

        self.scrn_width = screen_width
        self.scrn_height = screen_height

        self.new_lvl = current_lvl

        # Each bug is now independent
        self.bugs = [self.new_bug(offset=i * 150) for i in range(8)]
        self.difficulty = 0

        
        
    def new_bug(self, offset=0):
        # Creates one bug with randomised properties
        return {
            'x': random.randint(0, int(self.scrn_width - 67)),
            'y': -random.randint(50, 400) - offset,  # staggered start heights
            'vel': random.uniform(3.5, 6.5),          # each bug slightly different speed
            'drift': random.uniform(-0.4, 0.4),       # slow horizontal wobble
        }
    
    def level_up(self, new_lvl):
        self.level = new_lvl
        for bug in self.bugs:
            # Give existing bugs a speed bump too
            direction = 1 if bug['vel'] > 0 else -1
            bug['vel'] = direction * (random.uniform(3.5, 6.5) + self.level)

    def draw(self, screen):

        if not self.enemies_available:
            return 
        
    
        for bug in self.bugs:
            self.move_bug(bug)

            img = self.enemies[0] if bug['vel'] > 0 else self.enemies_l[0]
            screen.blit(img, (bug['x'], bug['y']))

    def move_bug(self, bug):
        bug['y'] += bug['vel']
        bug['x'] += bug['drift']

        if bug['x'] <= 0 or bug['x'] >= self.scrn_width - 67:
            bug['drift'] *= -1

        if bug['vel'] > 0 and bug['y'] > self.scrn_height + random.randint(30, 120):
            # random flip point breaks phase convergence
            bug['vel'] = -(random.uniform(3.5, 6.5) + self.level)  # level bonus added ✅
            bug['drift'] = random.uniform(-0.4, 0.4)

        if bug['vel'] < 0 and bug['y'] < -random.randint(200, 500):
            # random re-entry point breaks phase convergence
            bug['vel'] = random.uniform(3.5, 6.5) + self.level     # level bonus added ✅
            bug['x'] = random.randint(0, int(self.scrn_width - 67))
            bug['drift'] = random.uniform(-0.4, 0.4)

    def enemy_mask(self):
        if any(b['vel'] > 0 for b in self.bugs):
            return self.enemy_mask_fwd
        return self.enemy_mask_bwd

    #def bug(self):
 #============================================================================
