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

# Load the images
background_image = pygame.image.load("background2.jpg").convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

character_image = pygame.image.load("character.png").convert_alpha()
character_width = 100
character_height = 100
character_image = pygame.transform.scale(character_image, (character_width, character_height))

ufo_image = pygame.image.load("ufo.png").convert_alpha()
ufo_width = 150
ufo_height = 100
ufo_image = pygame.transform.scale(ufo_image, (ufo_width, ufo_height))

beam_image = pygame.image.load("beam.png").convert_alpha()
beam_width = 20
beam_height = 50
beam_image = pygame.transform.scale(beam_image, (beam_width, beam_height))

life_bar_width = 200
life_bar_height = 20

# Set initial positions
character_x = 0
character_y = screen_height - character_height

ufo_x = (screen_width - ufo_width) // 2
ufo_y = 100

ufo2_x = 0
ufo2_y = 100

beam_x = -beam_width
beam_y = -beam_height

character_speed = 5
is_jumping = False
jump_count = 10

ufo_speed = 2
ufo2_speed = 2

beam_speed = 5
beam_active = False
beam_timer = 0
beam_interval = random.randint(2000, 4000)

beam2_active = False
beam2_timer = 0
beam2_interval = random.randint(2000, 4000)

score = 0
hit_beams = 0
life = 100

pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)

start_game = False
clock = pygame.time.Clock()

while not start_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            start_game = True

    screen.blit(background_image, (0, 0))
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

    if character_x < ufo_x:
        ufo_x -= ufo_speed
    elif character_x > ufo_x:
        ufo_x += ufo_speed

    if ufo_x < 0:
        ufo_x = 0
    elif ufo_x > screen_width - ufo_width:
        ufo_x = screen_width - ufo_width

    # Update the position of the second UFO
    if ufo2_x < screen_width - ufo_width:
        ufo2_x += ufo2_speed
    else:
        ufo2_x = 0

    if beam_active:
        beam_y += beam_speed
        if beam_y > screen_height:
            beam_active = False
            score += 5

        if character_x < beam_x + beam_width and character_x + character_width > beam_x \
                and character_y < beam_y + beam_height and character_y + character_height > beam_y:
            hit_beams += 1
            beam_active = False
            life -= 20

    if beam2_active:
        beam2_y += beam_speed
        if beam2_y > screen_height:
            beam2_active = False
            score += 5

        if character_x < beam2_x + beam_width and character_x + character_width > beam2_x \
                and character_y < beam2_y + beam_height and character_y + character_height > beam2_y:
            hit_beams += 1
            beam2_active = False
            life -= 20

    if not beam_active:
        beam_timer += clock.get_time()
        if beam_timer >= beam_interval:
            beam_x = ufo_x + ufo_width // 2 - beam_width // 2
            beam_y = ufo_y + ufo_height
            beam_active = True
            beam_timer = 0
            beam_interval = random.randint(2000, 4000)

    if not beam2_active:
        beam2_timer += clock.get_time()
        if beam2_timer >= beam2_interval:
            beam2_x = ufo2_x + ufo_width // 2 - beam_width // 2
            beam2_y = ufo2_y + ufo_height
            beam2_active = True
            beam2_timer = 0
            beam2_interval = random.randint(2000, 4000)

    screen.blit(background_image, (0, 0))
    screen.blit(character_image, (character_x, character_y))
    screen.blit(ufo_image, (ufo_x, ufo_y))
    screen.blit(ufo_image, (ufo2_x, ufo2_y))
    if beam_active:
        screen.blit(beam_image, (beam_x, beam_y))
    if beam2_active:
        screen.blit(beam_image, (beam2_x, beam2_y))

    # Draw the life bar
    pygame.draw.rect(screen, (255, 0, 0), (screen_width - life_bar_width - 20, 20, life_bar_width, life_bar_height))
    life_bar_fill = max(0, life / 100) * life_bar_width
    pygame.draw.rect(screen, (0, 255, 0), (screen_width - life_bar_width - 20, 20, life_bar_fill, life_bar_height))

    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    hit_text = font.render("Hits: " + str(hit_beams), True, (255, 255, 255))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 10))
    screen.blit(hit_text, (10, 10))

    if life <= 0:
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()