import pygame, random
import sys
from settings import *
from game_functions import *

# Function to reset the game state
def reset_game():
    global game_active, player_score, scroll_sky, scroll_ground, snail1_speed, snail2_speed, moving_left, moving_right, is_midair, player_gravity, scored_snail1, scored_snail2
    game_active = True
    player_score = 0
    snail1_speed = 3
    snail2_speed = 2
    moving_left = False
    moving_right = False
    is_midair = False
    scored_snail1 = False
    scored_snail2 = False
    player_rect.midbottom = (50, 310)
    player_gravity = 0
    snail1_rect.midbottom = (SCREEN_WIDTH, snail_y)
    snail2_rect.midbottom = (SCREEN_WIDTH, snail_y)

# Function to handle key press events
def handle_key_presses(event):
    global moving_left, moving_right
    if event.key == pygame.K_d:
        moving_right = True
    elif event.key == pygame.K_a:
        moving_left = True

# Function to handle key release events
def handle_key_releases(event):
    global moving_left, moving_right
    if event.key == pygame.K_d:
        moving_right = False
    elif event.key == pygame.K_a:
        moving_left = False

# Function to update the player's position based on key input
def update_player_position():
    global moving_left, moving_right, is_midair
    if moving_right and not is_midair:
        player_rect.x += 5
    if moving_left and not is_midair:
        player_rect.x -= 5
    if player_rect.left < 0:
        player_rect.left = 0
    if player_rect.right > SCREEN_WIDTH:
        player_rect.right = SCREEN_WIDTH
    if player_rect.bottom >= 310:
        is_midair = False

# Function to update the score surface
def update_score_surface():
    global score_surf, score_rect
    score_background = pygame.Surface((score_rect.width, score_rect.height))
    score_background.fill((0, 0, 0))
    screen.blit(score_background, score_rect)
    player_score_surf = test_font.render('SCORE:    ' + str(player_score), False, 'White')
    score_rect = player_score_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50))
    screen.blit(player_score_surf, score_rect)

# Function to draw game objects on the screen
def draw_objects():
    for i in range(0, tiles):
        screen.blit(sky_surface, (i * sky_width + scroll_sky, 0))
    for i in range(0, tiles):
        screen.blit(ground_surface, (i * ground_width + scroll_ground, 310))
    screen.blit(snail1_surface, snail1_rect)
    screen.blit(snail2_surface, snail2_rect)
    screen.blit(player_surface, player_rect)

# Function to update the positions of the snails and handle scoring
def update_snails():
    global snail1_speed, snail2_speed, player_score
    snail1_rect.x -= snail1_speed
    snail2_rect.x -= snail2_speed
    if snail1_rect.right <= 0:
        snail1_rect.left = SCREEN_WIDTH
        snail1_speed = random.randint(3, 8)
        player_score += 1
    if snail2_rect.right <= 0:
        snail2_rect.left = SCREEN_WIDTH
        snail2_speed = random.randint(3, 8)
        player_score += 1
    score_surf = test_font.render('SCORE:    ' + str(player_score), False, 'White')

# Function to handle events when the game is over
def handle_game_over(event):
    if event.key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()
    elif event.key == pygame.K_SPACE and game_active == False:
        reset_game()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_midair and game_active:
                player_gravity = -18
                is_midair = True
            elif not game_active:
                handle_game_over(event)
            else:
                handle_key_presses(event)

        elif event.type == pygame.KEYUP:
            handle_key_releases(event)

    if game_active:
        update_player_position()
        draw_objects()
        scroll_sky -= 0.25
        scroll_ground -= 1
        if abs(scroll_sky) > sky_width:
            scroll_sky = 0
        if abs(scroll_ground) > ground_width:
            scroll_ground = 0
        update_score_surface()
        update_snails()
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 310:
            player_rect.bottom = 310
        if snail1_rect.colliderect(player_rect) or snail2_rect.colliderect(player_rect):
            game_active = False
    else:
        screen.fill('Black')
        screen.blit(end_surf, (SCREEN_WIDTH // 2 - end_surf.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(end_continue_surf, (SCREEN_WIDTH // 2 - end_continue_surf.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(end_exit_surf, (SCREEN_WIDTH // 2 - end_exit_surf.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        player_score_surf = test_font.render('SCORE:    ' + str(player_score), False, 'White')
        score_rect = player_score_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(player_score_surf, score_rect)

    pygame.display.update()
    clock.tick(60)
