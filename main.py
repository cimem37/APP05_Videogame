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

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw on the screen
    screen.blit(background_image, (0, 0))  # Draw the background image at (0, 0)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
