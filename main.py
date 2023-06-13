import pygame
import sys
import random
import math

BASE_PATH = 'C:/Users/Kitsa/OneDrive/Desktop/pyrunner/pygame_runner'
font_path = BASE_PATH + '/fonts/pixeltype.ttf'
image_path = BASE_PATH + '/graphics/'
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1200
snails = []
scored_snails = []
max_snails = 4  # Maximum number of snails on the screen at a time

# Initialize game state variables
game_active = True
player_score = 0
scroll_sky = 0
scroll_ground = 0
snail_y = 310
snail1_speed = 3
snail2_speed = 2
moving_left = False
moving_right = False
is_midair = False

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Test Game')
clock = pygame.time.Clock()
test_font = pygame.font.Font(font_path, 50)

sky_surface = pygame.image.load(image_path + 'sky.png').convert()
ground_surface = pygame.image.load(image_path + 'ground.png').convert()
score_surf = test_font.render(str(player_score), False, 'White')
end_surf = test_font.render('Game Over', False, 'White')
end_continue_surf = test_font.render('Press SPACE to continue', False, 'White')
end_exit_surf = test_font.render('Press ESCAPE to exit', False, 'White')

score_rect = score_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50))
snail1_surface = pygame.image.load(image_path + 'snail/snail1.png').convert_alpha()
snail1_rect = snail1_surface.get_rect(midbottom=(SCREEN_WIDTH, snail_y))

snail2_surface = pygame.image.load(image_path + 'snail/snail2.png').convert_alpha()
snail2_rect = snail2_surface.get_rect(midbottom=(SCREEN_WIDTH, snail_y))

player_surface = pygame.image.load(image_path + 'player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom=(50, 310))
player_gravity = 0

sky_width = sky_surface.get_width()
ground_width = ground_surface.get_width()
tiles = math.ceil(SCREEN_WIDTH / sky_width) + 1


class Snail:
    def __init__(self, x, speed):
        self.surface = pygame.image.load(image_path + 'snail/snail1.png').convert_alpha()
        self.rect = self.surface.get_rect(midbottom=(x, snail_y))
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right <= 0:
            self.rect.left = SCREEN_WIDTH
            self.speed = random.randint(3, 8)


# Create initial snails
for _ in range(max_snails):
    x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH * 2)
    speed = random.randint(3, 8)
    snail = Snail(x, speed)
    snails.append(snail)


def reset_game():
    # Reset game state variables
    global game_active, player_score, scroll_sky, scroll_ground, snail1_speed, snail2_speed, moving_left, moving_right, is_midair, scored_snails, score_surf
    game_active = True
    scored_snails = set()
    player_score = 0
    score_surf = test_font.render(str(player_score), False, 'White')  # Clear the player score
    scroll_sky = 0
    scroll_ground = 0
    snail1_speed = 3
    snail2_speed = 2
    moving_left = False
    moving_right = False
    is_midair = False
    # Reset player position
    player_rect.midbottom = (50, 310)
    player_gravity = 0
    # Reset snail positions
    snail1_rect.midbottom = (SCREEN_WIDTH, snail_y)
    snail2_rect.midbottom = (SCREEN_WIDTH, snail_y)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Jump if space key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_midair and game_active:
                player_gravity = -18
                is_midair = True

            # Check for game restart
            if not game_active:
                if event.key == pygame.K_SPACE:
                    reset_game()

        # Check for key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_a:
                moving_left = True

        # Check for key releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_a:
                moving_left = False

    # Update the game state
    if moving_right and not is_midair:
        player_rect.x += 5
    if moving_left and not is_midair:
        player_rect.x -= 5

    if player_rect.bottom >= 310:
        is_midair = False

    if game_active:
        # Draw background
        for i in range(0, tiles):
            screen.blit(sky_surface, (i * sky_width + scroll_sky, 0))
        for i in range(0, tiles):
            screen.blit(ground_surface, (i * ground_width + scroll_ground, 310))

        # Scroll background
        scroll_sky -= 0.25
        scroll_ground -= 1

        # Reset scroll
        if abs(scroll_sky) > sky_width:
            scroll_sky = 0
        if abs(scroll_ground) > ground_width:
            scroll_ground = 0

        # Move and draw snails
        for snail in snails:
            snail.update()
            screen.blit(snail.surface, snail.rect)

            # Check if player jumped over a snail
            if snail.rect.right < player_rect.left and snail.rect not in scored_snails:
                scored_snails.append(snail.rect)
                player_score += 10
                score_surf = test_font.render(str(player_score), False, 'White')

        # Draw player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 310:
            player_rect.bottom = 310
        screen.blit(player_surface, player_rect)

        # Draw text
        score_surf = test_font.render(str(player_score), False, 'White')
        score_rect = score_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50))
        screen.blit(score_surf, score_rect)

        # Check if snails collide with the player
        for snail in snails:
            for rect in scored_snails:
                if rect.colliderect(player_rect):
                    game_active = False
                    break

    else:
        # Display game over screen
        screen.fill('Black')
        screen.blit(score_surf, score_rect)
        screen.blit(end_surf, (400, 200))
        screen.blit(end_continue_surf, (400, 240))
        screen.blit(end_exit_surf, (400, 280))

        # Handle game restart in the game over state
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            elif event.key == pygame.K_SPACE:
                reset_game()

    pygame.display.update()
    clock.tick(60)
 