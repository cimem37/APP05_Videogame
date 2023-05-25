import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Window")

# Load the background image
background_image = pygame.image.load("background2.jpg").convert()

# Scale the background image to fit the screen
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Load the background music
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)  # Play the background music indefinitely (-1)

# Load the "Press any key to start" image
press_image = pygame.image.load("press_signal.png").convert_alpha()

# Get the dimensions of the press image
press_width = press_image.get_width()
press_height = press_image.get_height()

# Position the press image at the top-middle of the screen
press_x = (screen_width - press_width) // 2
press_y = screen_height // 4

# Variables for controlling the flashing effect
fade_alpha = 255  # Initial alpha value (fully opaque)
fade_speed = 3    # Speed of fading (lower values mean slower fading)
fade_direction = 1  # Direction of fading (1 = fade in, -1 = fade out)

# Game loop
start_game = False
clock = pygame.time.Clock()

while not start_game:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            start_game = True

    # Flashing effect for the press image
    fade_alpha += fade_direction * fade_speed
    if fade_alpha > 255:
        fade_alpha = 255
        fade_direction = -1
    elif fade_alpha < 0:
        fade_alpha = 0
        fade_direction = 1

    # Draw on the screen
    screen.blit(background_image, (0, 0))  # Draw the background image at (0, 0)
    press_image.set_alpha(fade_alpha)  # Set the alpha value for fading effect
    screen.blit(press_image, (press_x, press_y))  # Draw the press image

    # Update the display
    pygame.display.flip()
    clock.tick(60)  # Limit the frame rate to 60 FPS

# Game logic and main game loop go here
# ...

# Quit Pygame
pygame.quit()
