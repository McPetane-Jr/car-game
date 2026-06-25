#Game info script:

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
