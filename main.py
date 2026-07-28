# Main script
import sys
import math
import random

import pygame

from car import car, Bombs
from entities import food, health, Enemy, fuel_image
from game_info import Game_info
from utils import blit_rotate_center, scale_image, resource_path

pygame.init()

# ---- Things that should only ever happen ONCE ----

# Screen size
small_scrn_width, small_scrn_height = 1280 * 0.9, 720 * 0.9
screen_width, screen_height = small_scrn_width, small_scrn_height

# Icon
icon_img = pygame.image.load(resource_path("icon.png"))
pygame.display.set_icon(icon_img)

# Background
bg = pygame.image.load(resource_path("bg.jpg"))

# Main menu background
def scale_menu_background(raw_menu_bg):
    """ 
    Scale the raw menu background image to fit the screen size while maintaining aspect ratio.

    """

    img_w, img_h = raw_menu_bg.get_size()

    scale = max(screen_width / img_w, screen_height / img_h) #

    new_w, new_h = round(img_w * scale), round(img_h * scale)

    scaled_menu_bg = pygame.transform.scale(raw_menu_bg, (new_w, new_h))

    # Crop centered to exactly screen_width x screen_height
    x_offset = (new_w - screen_width) // 2
    y_offset = (new_h - screen_height) // 2
    return scaled_menu_bg.subsurface((x_offset, y_offset, screen_width, screen_height)).copy()

menu_bg = scale_menu_background(pygame.image.load(resource_path("ChatGPT cyberbug Image.png")))
menu_font_title = pygame.font.SysFont("arial", 60, bold=True)
menu_font_prompt = pygame.font.SysFont("arial", 28)

# Screen + clock
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("CAR")
clock = pygame.time.Clock()

# Invisible surface: for drawing entities so the bg is the only thing that wiggles
frame_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)


# Music (loaded once, played/paused as needed)
pygame.mixer.music.load(resource_path(
    'Here Comes a Thought - Steven Universe karaoke [Official Instrumental](MP3_160K).mp3'
))
pygame.mixer.music.set_volume(0.5)

# ---- Globals that get created/reset each time play() runs ----
mute = False
collision_cooldown = 0
COLLISION_COOLDOWN_MS = 400  # ms between fuel drain hits

game = None
centipedes = None
cyberBug = None
bomb = None
fuel_icon = None
hp = None
keys = None


    

def animate():
    screen.blit(bg, (0, 0))
    fuel_icon.draw(screen)
    cyberBug.draw(screen)
    hp.draw(screen)
    centipedes.draw(screen)
    bomb.draw(screen, 20, 45)
    pygame.display.update()


def buttons():
    moving = False

    if keys[pygame.K_v]:
        cyberBug.shield_active = True     # V -> shield

    if keys[pygame.K_f]:
        bomb.detonate()
    else:
        bomb.F_down = False

    if keys[pygame.K_g]:
        if bomb.count > 0 and not bomb.exploded:
            bomb.solid = False
            bomb.exploded = True

    if keys[pygame.K_SPACE]:
        cyberBug.max_vel = 17
        cyberBug.rotation_vel = 9
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

    if keys[pygame.K_RIGHT]:
        cyberBug.rotation(right=True)
        cyberBug.rotation(left=False)
        bomb.x, bomb.y = cyberBug.x, cyberBug.y

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


def collision_cntrl():
    global collision_cooldown

    if cyberBug.hit(fuel_icon.col(), fuel_icon.x, fuel_icon.y) is not None:
        hp.fuel += 12.5
        game.progress += 1
        hp.score += 1
        fuel_icon.collided()

    now = pygame.time.get_ticks()

    for bug in centipedes.bugs:
        mask = centipedes.get_bug_mask(bug)
        if cyberBug.hit(mask, bug['x'], bug['y']) is not None:
            if now > collision_cooldown:
                hp.fuel -= 2.125
                collision_cooldown = now + COLLISION_COOLDOWN_MS

                bug_direction = 1 if bug['vel'] > 0 else -1
                cyberBug.vel = -bug_direction * min(abs(bug['vel']), 8)
            break


def main_menu():
    """
    Shows the menu background and waits for a left-click to start.
    Returns "play" when the player clicks, or exits on window close.
    """
    prompt_visible = True
    blink_timer = 0

    menu_running = True
    while menu_running:
        clock.tick(32)
        blink_timer += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Game closed by user.")
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                menu_running = False

        screen.blit(menu_bg, (0, 0))

        title_surf = menu_font_title.render("CYBERBUG", True, "red")
        screen.blit(title_surf, (screen_width / 2 - title_surf.get_width() / 2, screen_height * 0.85))

        # Simple blink effect so the prompt doesn't just sit there static
        if blink_timer % 32 < 20:
            prompt_surf = menu_font_prompt.render("Click to Start", True, (255, 255, 255))
            screen.blit(prompt_surf, (screen_width / 2 - prompt_surf.get_width() / 2, screen_height*0.8))

        pygame.display.update()

    return "play"


def pause_menu():
    """
    Placeholder for a pause overlay, triggered by e.g. ESC during play().
    """
    pass


def game_over_screen():
    """
    Placeholder for a game-over / score screen shown when hp.fuel
    runs out permanently, or the player dies another way.
    Should eventually return "retry", "menu", or "quit".
    """
    pass


def play():
    global mute, collision_cooldown, keys
    global game, centipedes, cyberBug, bomb, fuel_icon, hp

    # Fresh game objects every time play() is called (new run / restart)
    game = Game_info()
    centipedes = Enemy(screen_width, screen_height, game.lvl)
    cyberBug = car(14, 20, 350, screen_width, screen_height)
    bomb = Bombs(4, 20, 350, screen_width, screen_height)
    fuel_icon = food(
        random.randint(5, 1000 - fuel_image.get_width() - 100),
        random.randint(0, 550 - fuel_image.get_height() - 50),
        screen_width, screen_height
    )
    hp = health(20, 20, 140, 20, 140, 140, screen_width, screen_height)

    collision_cooldown = 0
    pygame.mixer.music.play(-1)

    start_game = True
    while start_game:
        clock.tick(32)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Game closed by user.")
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    mute = not mute
                    if mute:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

        keys = pygame.key.get_pressed()

        buttons()
        collision_cntrl()
        hp.save_score()

        if game.progress // 5 == game.lvl and game.progress > 0:
            game.next_lvl()
            centipedes.level_up(game.lvl)

        if game.lvl > 1:
            centipedes.enemies_available = True

        animate()


# ---- Entry point ----

def run_game():
    state = "menu"
    while state != "quit":
        if state == "menu":
            state = main_menu()
        elif state == "play":
            play()
            state = "menu"


run_game()