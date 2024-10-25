import random
import pygame
from spritesheet import SpriteSheet

# Constants
CONTROLLER_INPUT = False

# Pygame Setup
pygame.init()
#screen = pygame.display.set_mode((1024, 600))
screen = pygame.display.set_mode((1024, 600), pygame.NOFRAME)
clock = pygame.time.Clock()
try:
    joystick = pygame.joystick.Joystick(0)
except pygame.error:
    print("No controller connected")
    CONTROLLER_INPUT = False

# Sprites
bg = pygame.image.load("../images/bg.png")
idle = SpriteSheet(pygame.image.load("../images/idle.png"), 32)
normal_talk = SpriteSheet(pygame.image.load("../images/normal_talking.png"), 8)
smile = SpriteSheet(pygame.image.load("../images/smile.png"), 64)
happy = SpriteSheet(pygame.image.load("../images/happy.png"), 64)

# SFX
talking_sfx = [pygame.mixer.Sound("../audio/talking_1.ogg"), pygame.mixer.Sound("../audio/talking_2.ogg"), pygame.mixer.Sound("../audio/talking_3.ogg"), pygame.mixer.Sound("../audio/talking_4.ogg")]
talking_sfx_index = 0

# General Variables
sprite_index = 0
face_sheet = idle
talking_pos = 0

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(bg, (0, 0))

    if CONTROLLER_INPUT:
        if joystick.get_button(7):  # R3(Joy) Button
            CONTROLLER_INPUT = False
        elif joystick.get_button(6):  # +(Plus/Start) Button
            face_sheet = normal_talk
        elif joystick.get_button(18):  # ZR Button
            face_sheet = smile
        elif joystick.get_button(16):  # R Button
            face_sheet = happy
        else:
            face_sheet = idle
    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
        elif keys[pygame.K_t]:
            face_sheet = normal_talk
            if not pygame.mixer.Channel(0).get_busy():
                talking_sfx_index = random.randint(0, 3)
                talking_sfx[talking_sfx_index].play(-1)
        elif keys[pygame.K_1]:
            face_sheet = smile
            talking_sfx[talking_sfx_index].stop()
        elif keys[pygame.K_2]:
            face_sheet = happy
            talking_sfx[talking_sfx_index].stop()
        else:
            face_sheet = idle
            talking_sfx[talking_sfx_index].stop()

    if face_sheet == idle:
        if random.randint(0, 25) == 0 and (sprite_index < 15 or sprite_index > 28):
            screen.blit(face_sheet.get_image(25, 64, 64, 8, (0, 0, 0)), (256, 44))
        else:
            screen.blit(face_sheet.get_image(sprite_index, 64, 64, 8, (0, 0, 0)), (256, 44))
    else:
        screen.blit(face_sheet.get_image(sprite_index, 64, 64, 8, (0, 0, 0)), (256, 44))

    if sprite_index < face_sheet.frame_count - 1:
        sprite_index += 1
    else:
        sprite_index = 0

    pygame.display.flip()

    clock.tick(15)

pygame.quit()
