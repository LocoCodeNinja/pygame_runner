import pygame
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, player_score, snail_y, screen, sky_width, ground_width, score_rect, snail1_speed, snail2_speed

# Initialize pygame
pygame.init()

# Set up file paths for game assets
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(BASE_PATH, 'fonts', 'pixeltype.ttf')
image_path = os.path.join(BASE_PATH, 'graphics')

# Load game assets
test_font = pygame.font.Font(font_path, 50)
sky_surface = pygame.image.load(os.path.join(image_path, 'sky.png')).convert()
ground_surface = pygame.image.load(os.path.join(image_path, 'ground.png')).convert()
score_surf = test_font.render("SCORE: " + str(player_score), False, 'White')
end_surf = test_font.render('Game Over', False, 'White')
end_continue_surf = test_font.render('Press SPACE to continue', False, 'White')
end_exit_surf = test_font.render('Press ESCAPE to exit', False, 'White')

snail1_surface = pygame.image.load(os.path.join(image_path, 'snail/snail1.png')).convert_alpha()
snail2_surface = pygame.image.load(os.path.join(image_path, 'snail/snail2.png')).convert_alpha()
player_surface = pygame.image.load(os.path.join(image_path, 'player/player_walk_1.png')).convert_alpha()

snail1_rect = snail1_surface.get_rect(midbottom=(SCREEN_WIDTH, snail_y))
snail2_rect = snail2_surface.get_rect(midbottom=(SCREEN_WIDTH, snail_y))
player_rect = player_surface.get_rect(midbottom=(50, 310))

def handle_key_presses(event):
    global moving_left, moving_right

    if event.key == pygame.K_LEFT:
        moving_left = True
    elif event.key == pygame.K_RIGHT:
        moving_right = True

def handle_key_releases(event):
    global moving_left, moving_right

    if event.key == pygame.K_LEFT:
        moving_left = False
    elif event.key == pygame.K_RIGHT:
        moving_right = False

def update_player_position():
    global moving_left, moving_right, is_midair, player_gravity

    if moving_left:
        player_rect.x -= 5
    elif moving_right:
        player_rect.x += 5

    if player_rect.left <= 0:
        player_rect.left = 0
    elif player_rect.right >= SCREEN_WIDTH:
        player_rect.right = SCREEN_WIDTH

    if is_midair:
        player_gravity += 1
    player_rect.y += player_gravity

    if player_rect.bottom >= 310:
        player_rect.bottom = 310
        is_midair = False
        player_gravity = 0

def update_score_surface():
    global score_surf, player_score

    score_surf = test_font.render("SCORE: " + str(player_score), False, 'White')

def draw_objects():
    global scroll_sky, scroll_ground

    screen.blit(sky_surface, (scroll_sky, 0))
    screen.blit(sky_surface, (sky_width + scroll_sky, 0))
    screen.blit(ground_surface, (scroll_ground, SCREEN_HEIGHT - ground_surface.get_height()))
    screen.blit(ground_surface, (ground_width + scroll_ground, SCREEN_HEIGHT - ground_surface.get_height()))
    screen.blit(player_surface, player_rect)
    screen.blit(snail1_surface, snail1_rect)
    screen.blit(snail2_surface, snail2_rect)
    screen.blit(score_surf, score_rect)

def update_snails():
    global snail1_rect, snail2_rect, scored_snail1, scored_snail2, player_score

    snail1_rect.x -= snail1_speed
    snail2_rect.x -= snail2_speed

    if snail1_rect.right <= 0:
        snail1_rect.left = SCREEN_WIDTH
        scored_snail1 = False
    if snail2_rect.right <= 0:
        snail2_rect.left = SCREEN_WIDTH
        scored_snail2 = False

    if not scored_snail1 and player_rect.right >= snail1_rect.left:
        player_score += 1
        scored_snail1 = True
    if not scored_snail2 and player_rect.right >= snail2_rect.left:
        player_score += 1
        scored_snail2 = True

def handle_game_over(event):
    global game_active, player_score

    if event.key == pygame.K_SPACE:
        reset_game()
    elif event.key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()

def reset_game():
    global game_active, scroll_sky, scroll_ground, player_score, snail1_rect, snail2_rect

    game_active = True
    scroll_sky = 0
    scroll_ground = 0
    player_score = 0
    snail1_rect = snail1_surface.get_rect(midbottom=(SCREEN_WIDTH, snail_y))
    snail2_rect = snail2_surface.get_rect(midbottom=(SCREEN_WIDTH, snail_y))

