import pygame
import sys
import random

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

# Load the character image
character_image = pygame.image.load("character.png").convert_alpha()
# Resize the character image
character_width = 100
character_height = 100
character_image = pygame.transform.scale(character_image, (character_width, character_height))

# Load the UFO image
ufo_image = pygame.image.load("ufo.png").convert_alpha()
# Resize the UFO image
ufo_width = 150
ufo_height = 100
ufo_image = pygame.transform.scale(ufo_image, (ufo_width, ufo_height))

# Load the beam image
beam_image = pygame.image.load("beam.png").convert_alpha()
# Resize the beam image
beam_width = 20
beam_height = 50
beam_image = pygame.transform.scale(beam_image, (beam_width, beam_height))

# Position the character at the middle of the left side of the bottom screen
character_x = 0
character_y = screen_height - character_height

# Position the UFO at the top-middle of the screen
ufo_x = (screen_width - ufo_width) // 2
ufo_y = 100

# Position the beam initially off-screen
beam_x = -beam_width
beam_y = -beam_height

# Variables for controlling the character movement
character_speed = 5
is_jumping = False
jump_count = 10

# Variables for controlling the UFO movement
ufo_speed = 2

# Variables for controlling the beam
beam_speed = 5
beam_active = False
beam_timer = 0
beam_interval = random.randint(2000, 4000)

# Variables for registering successful beam hits
hits = 0

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

    # Draw on the screen
    screen.blit(background_image, (0, 0))  # Draw the background image

    # Update the display
    pygame.display.flip()
    clock.tick(60)  # Limit the frame rate to 60 FPS

# Main game loop
while True:
    # Event handling
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

    # Jumping animation
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

    # Ensure the character stays within the screen boundaries
    if character_x < 0:
        character_x = 0
    elif character_x > screen_width - character_width:
        character_x = screen_width - character_width

    # Update the UFO position to chase the character
    if character_x < ufo_x:
        ufo_x -= ufo_speed
    elif character_x > ufo_x:
        ufo_x += ufo_speed

    # Ensure the UFO stays within the screen boundaries
    if ufo_x < 0:
        ufo_x = 0
    elif ufo_x > screen_width - ufo_width:
        ufo_x = screen_width - ufo_width

    # Update the beam position and state
    if beam_active:
        beam_y += beam_speed
        if beam_y > screen_height:
            beam_active = False

        # Check for collision with the character
        if character_x < beam_x + beam_width and character_x + character_width > beam_x \
                and character_y < beam_y + beam_height and character_y + character_height > beam_y:
            # Register successful beam hit on the character
            hits += 1
            beam_active = False

    # Shoot beam at regular intervals
    if not beam_active:
        beam_timer += clock.get_time()
        if beam_timer >= beam_interval:
            beam_x = ufo_x + ufo_width // 2 - beam_width // 2
            beam_y = ufo_y + ufo_height
            beam_active = True
            beam_timer = 0
            beam_interval = random.randint(2000, 4000)

    # Draw on the screen
    screen.blit(background_image, (0, 0))  # Draw the background image
    screen.blit(character_image, (character_x, character_y))  # Draw the character
    screen.blit(ufo_image, (ufo_x, ufo_y))  # Draw the UFO
    if beam_active:
        screen.blit(beam_image, (beam_x, beam_y))  # Draw the beam

    # Display the number of successful beam hits
    font = pygame.font.Font(None, 36)
    text = font.render("Hits: " + str(hits), True, (255, 255, 255))
    screen.blit(text, (10, 10))

    # Update the display
    pygame.display.flip()
    clock.tick(60)  # Limit the frame rate to 60 FPS

# Quit Pygame
pygame.quit()
sys.exit()
