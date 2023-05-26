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

ufo2_image = pygame.image.load("leufo.png").convert_alpha()
ufo2_width = 150
ufo2_height = 100
ufo2_image = pygame.transform.scale(ufo2_image, (ufo2_width, ufo2_height))

beam_image = pygame.image.load("beam.png").convert_alpha()
beam_width = 20
beam_height = 50
beam_image = pygame.transform.scale(beam_image, (beam_width, beam_height))

# Set initial positions
character_x = screen_width // 2 - character_width // 2
character_y = screen_height - character_height

ufo_x = (screen_width - ufo_width) // 2
ufo_y = 100

ufo2_x = 0
ufo2_y = 200

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
health = 100

# Load the font
font = pygame.font.Font(None, 36)

# Load the sounds
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)
beam_sound = pygame.mixer.Sound("beam_sound.wav")
hit_sound = pygame.mixer.Sound("hit_sound.wav")

# Game start screen
start_game = False
clock = pygame.time.Clock()

# Fade settings
fade_duration = 1000
fade_alpha = 0
fade_in = True
fade_timer = 0

# Press signal settings
press_signal_image = pygame.image.load("press_signal.png").convert_alpha()
press_signal_width = press_signal_image.get_width()
press_signal_height = press_signal_image.get_height()
press_signal_x = screen_width // 2 - press_signal_width // 2
press_signal_y = screen_height // 2 - press_signal_height // 2

# Health bar settings
health_bar_width = 200
health_bar_height = 20
health_bar_x = screen_width // 2 - health_bar_width // 2
health_bar_y = 20

def draw_health_bar():
    pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
    current_health = max(health, 0)
    pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, current_health / 100 * health_bar_width, health_bar_height))

def game_over():
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2))

while not start_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            start_game = True
    fade_timer += clock.get_time()

    if fade_in:
        fade_alpha = min(int((fade_timer / fade_duration) * 255), 255)
    else:
        fade_alpha = max(255 - int((fade_timer / fade_duration) * 255), 0)

    if fade_in and fade_timer >= fade_duration:
        fade_in = False
        fade_timer = 0

    if not fade_in and fade_timer >= fade_duration:
        fade_in = True
        fade_timer = 0

    screen.fill((0, 0, 0))
    screen.blit(background_image, (0, 0))

    press_signal_image.set_alpha(fade_alpha)
    screen.blit(press_signal_image, (press_signal_x, press_signal_y))

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
        if character_x < 0:
            character_x = 0
    elif keys[pygame.K_RIGHT]:
        character_x += character_speed
        if character_x > screen_width - character_width:
            character_x = screen_width - character_width

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

    if character_x < ufo_x:
        ufo_x -= ufo_speed
        if ufo_x < 0:
            ufo_x = 0
    elif character_x > ufo_x:
        ufo_x += ufo_speed
        if ufo_x > screen_width - ufo_width:
            ufo_x = screen_width - ufo_width

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
            hit_sound.play()
            health -= 10

    if beam2_active:
        beam2_y += beam_speed
        if beam2_y > screen_height:
            beam2_active = False
            score += 5

        if character_x < beam2_x + beam_width and character_x + character_width > beam2_x \
                and character_y < beam2_y + beam_height and character_y + character_height > beam2_y:
            hit_beams += 1
            beam2_active = False
            hit_sound.play()
            health -= 10

    if not beam_active and not beam2_active:
        if pygame.time.get_ticks() - beam_timer >= beam_interval:
            if random.randint(0, 1) == 0:
                beam_x = ufo_x + ufo_width // 2 - beam_width // 2
                beam_y = ufo_y + ufo_height
                beam_active = True
            else:
                beam2_x = ufo2_x + ufo2_width // 2 - beam_width // 2
                beam2_y = ufo2_y + ufo2_height
                beam2_active = True

            beam_timer = pygame.time.get_ticks()
            beam_interval = random.randint(2000, 4000)
            beam_sound.play()

    screen.fill((0, 0, 0))
    screen.blit(background_image, (0, 0))

    screen.blit(character_image, (character_x, character_y))
    screen.blit(ufo_image, (ufo_x, ufo_y))
    screen.blit(ufo2_image, (ufo2_x, ufo2_y))

    if beam_active:
        screen.blit(beam_image, (beam_x, beam_y))
    if beam2_active:
        screen.blit(beam_image, (beam2_x, beam2_y))

    draw_health_bar()

    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    hit_beams_text = font.render("Hit Beams: " + str(hit_beams), True, (255, 255, 255))
    screen.blit(hit_beams_text, (10, 50))

    if health <= 0:
        game_over()
        pygame.mixer.music.stop()
        break

    pygame.display.flip()
    clock.tick(60)
