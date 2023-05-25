import pygame
import sys
import random

# Initialize Pygame
pygame.init()


screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Window")


background_image = pygame.image.load("background2.jpg").convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

character_image = pygame.image.load("character.png").convert_alpha()
character_width = 100
character_height = 100
character_image = pygame.transform.scale(character_image, (character_width, character_height))

ufo_image = pygame.image.load("ufo.png").convert_alpha()
ufo_width = 100
ufo_height = 100
ufo_image = pygame.transform.scale(ufo_image, (ufo_width, ufo_height))

projectile_image = pygame.image.load("beam.png").convert_alpha()
projectile_width = 30
projectile_height = 30
projectile_image = pygame.transform.scale(projectile_image, (projectile_width, projectile_height))

character_x = 0
character_y = screen_height - character_height

ufo_x = (screen_width - ufo_width) // 2
ufo_y = 100

projectile_x = ufo_x + ufo_width // 2 - projectile_width // 2
projectile_y = ufo_y + ufo_height

character_speed = 5
is_jumping = False
jump_count = 10

ufo_speed = 3
is_ufo_moving_right = True

projectile_speed = 6
is_projectile_active = False

pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)  # Play the background music indefinitely (-1)

press_image = pygame.image.load("press_signal.png").convert_alpha()
press_width = press_image.get_width()
press_height = press_image.get_height()

press_x = (screen_width - press_width) // 2
press_y = screen_height // 4

fade_alpha = 255  # Initial alpha value (fully opaque)
fade_speed = 3    # Speed of fading (lower values mean slower fading)
fade_direction = 1  # Direction of fading (1 = fade in, -1 = fade out)

start_game = False
clock = pygame.time.Clock()

while not start_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            start_game = True
    fade_alpha += fade_direction * fade_speed
    if fade_alpha > 255:
        fade_alpha = 255
        fade_direction = -1
    elif fade_alpha < 0:
        fade_alpha = 0
        fade_direction = 1

    screen.blit(background_image, (0, 0))  # Draw the background image at (0, 0)
    press_image.set_alpha(fade_alpha)  # Set the alpha value for fading effect
    screen.blit(press_image, (press_x, press_y))  # Draw the press image

    # Update the display
    pygame.display.flip()
    clock.tick(60)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        character_x -= character_speed
        character_image_flipped = pygame.transform.flip(character_image, True, False)
        screen.blit(character_image_flipped, (character_x, character_y))
    elif keys[pygame.K_RIGHT]:
        character_x += character_speed
        screen.blit(character_image, (character_x, character_y))
    else:
        screen.blit(character_image, (character_x, character_y))

    if not is_jumping:
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            is_jumping = True

    if is_jumping:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            character_y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jumping = False
            jump_count = 10

    if character_x < 0:
        character_x = 0
    elif character_x > screen_width - character_width:
        character_x = screen_width - character_width

    if is_ufo_moving_right:
        ufo_x += ufo_speed
        if ufo_x > screen_width - ufo_width:
            ufo_x = screen_width - ufo_width
            is_ufo_moving_right = False
    else:
        ufo_x -= ufo_speed
        if ufo_x < 0:
            ufo_x = 0
            is_ufo_moving_right = True

    # Projectile logic
    if not is_projectile_active:
        # Calculate the position of the projectile relative to the UFO
        projectile_x = ufo_x + ufo_width // 2 - projectile_width // 2
        projectile_y = ufo_y + ufo_height


        is_projectile_active = True

    # Move the projectile downwards
    if is_projectile_active:
        projectile_y += projectile_speed

        # Check if the projectile has reached the character
        if projectile_y > character_y + character_height:
            is_projectile_active = False

    # Draw on the screen
    screen.blit(background_image, (0, 0))  # Draw the background image at (0, 0)
    screen.blit(character_image, (character_x, character_y))  # Draw the character
    screen.blit(ufo_image, (ufo_x, ufo_y))  # Draw the UFO

    if is_projectile_active:
        screen.blit(projectile_image, (projectile_x, projectile_y))  # Draw the projectile

    # Update the display
    pygame.display.flip()
    clock.tick(60)  # Limit the frame rate to 60 FPS

# End the game
pygame.quit()
sys.exit()
