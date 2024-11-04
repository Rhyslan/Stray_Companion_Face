import random
import pygame
from spritesheet import SpriteSheet

# Constants
CONTROLLER_INPUT = True

# Pygame Setup
pygame.init()
screen = pygame.display.set_mode((1024, 600), pygame.NOFRAME)
clock = pygame.time.Clock()
try:
    joystick = pygame.joystick.Joystick(0)
except pygame.error:
    print("No controller connected")
    CONTROLLER_INPUT = False

# Sprites
bg = pygame.image.load("../images/Blue_Background.png")
bg.set_alpha(200)
fg = pygame.image.load("../images/Pixel_Cells.png")
fg.set_alpha(40)

idle = SpriteSheet(pygame.image.load("../images/default_idle.png"), 32)
normal_talk = SpriteSheet(pygame.image.load("../images/normal_talking.png"), 8)
smile = SpriteSheet(pygame.image.load("../images/smile.png"), 64)
happy = SpriteSheet(pygame.image.load("../images/happy.png"), 64)
happy_talk = SpriteSheet(pygame.image.load("../images/happy_talking.png"), 8)
annoyed = SpriteSheet(pygame.image.load("../images/annoyed_idle.png"), 32)
annoyed_talk = SpriteSheet(pygame.image.load("../images/annoyed_talk.png"), 8)

# SFX
happy_talking = pygame.mixer.Sound("../audio/happy_talking.ogg")
talking = pygame.mixer.Sound("../audio/talking.ogg")
annoyed_talking = pygame.mixer.Sound("../audio/annoyed.ogg")

# General Variables
sprite_index = 0
face = idle
is_happy = False
is_annoyed = False
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(bg, (0, 0))

    # region Controller Input
    if CONTROLLER_INPUT:
        if joystick.get_button(7):      # R3(Joy) Button - disable controller input
            CONTROLLER_INPUT = False
        elif joystick.get_button(18):    # ZR Button - idle animation
            face = idle
            is_happy = False
            is_annoyed = False
            talking.stop()
            happy_talking.stop()
            annoyed_talking.stop()
        elif joystick.get_button(0):    # X Button - smile (small smile) animation
            face = smile
            is_happy = False
            is_annoyed = False
            talking.stop()
            happy_talking.stop()
            annoyed_talking.stop()
        elif joystick.get_button(1):    # A Button - happy (big smile) animation
            face = happy
            is_happy = True
            is_annoyed = False
            talking.stop()
            happy_talking.stop()
            annoyed_talking.stop()
        elif joystick.get_button(2):    # Y Button - annoyed animation
            face = annoyed
            is_happy = False
            is_annoyed = True
            talking.stop()
            happy_talking.stop()
            annoyed_talking.stop()
        elif joystick.get_button(6):    # +(Plus/Start) Button - talking animation with sfx
            if is_happy:
                face = happy_talk
                if not pygame.mixer.Channel(0).get_busy():
                    happy_talking.play(-1)
            elif is_annoyed:
                face = annoyed_talk
                if not pygame.mixer.Channel(0).get_busy():
                    annoyed_talking.play(-1)
            else:
                face = normal_talk
                if not pygame.mixer.Channel(0).get_busy():
                    talking.play(-1)
        elif joystick.get_button(16):   # R Button - silent talking animation
            if is_happy:
                face = happy_talk
            elif is_annoyed:
                face = annoyed_talk
            else:
                face = normal_talk
    # endregion Controller Input

    # region Keyboard Input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:           # Stop the program
        running = False
    elif keys[pygame.K_1]:              # Idle (default face) animation
        face = idle
        is_happy = False
        is_annoyed = False
        talking.stop()
        happy_talking.stop()
        annoyed_talking.stop()
    elif keys[pygame.K_2]:              # Smile (small smile) animation
        face = smile
        is_happy = False
        is_annoyed = False
        talking.stop()
        happy_talking.stop()
        annoyed_talking.stop()
    elif keys[pygame.K_3]:              # Happy (big smile) animation
        face = happy
        is_happy = True
        is_annoyed = False
        talking.stop()
        happy_talking.stop()
        annoyed_talking.stop()
    elif keys[pygame.K_4]:              # Annoyed animation
        face = annoyed
        is_happy = False
        is_annoyed = True
        talking.stop()
        happy_talking.stop()
        annoyed_talking.stop()
    elif keys[pygame.K_5]:              # Talking animation with sfx
        if is_happy:
            face = happy_talk
            if not pygame.mixer.Channel(0).get_busy():
                happy_talking.play(-1)
        elif is_annoyed:
            face = annoyed_talk
            if not pygame.mixer.Channel(0).get_busy():
                annoyed_talking.play(-1)
        else:
            face = normal_talk
            if not pygame.mixer.Channel(0).get_busy():
                talking.play(-1)
    elif keys[pygame.K_SPACE]:          # Silent talking animation
        if is_happy:
            face = happy_talk
        elif is_annoyed:
            face = annoyed_talk
        else:
            face = normal_talk
    # endregion Keyboard Input


    if face == idle:
        if random.randint(0, 25) == 0 and (sprite_index < 15 or sprite_index > 28):
            screen.blit(face.get_image(25, 64, 64, 8, (0, 0, 0)), (256, 44))
        else:
            screen.blit(face.get_image(sprite_index, 64, 64, 8, (0, 0, 0)), (256, 44))
    else:
        screen.blit(face.get_image(sprite_index, 64, 64, 8, (0, 0, 0)), (256, 44))

    screen.blit(fg, (0, 0))

    if sprite_index < face.frame_count - 1:
        sprite_index += 1
    else:
        sprite_index = 0

    pygame.display.flip()

    clock.tick(15)

pygame.quit()
