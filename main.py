import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Window")

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game logic

    # Draw on the screen
    screen.fill((255, 255, 255))  # Fill the screen with white
    # Add your drawing code here

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
