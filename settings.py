import pygame
import os
import math

# Set up file paths for game assets
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(BASE_PATH, 'fonts', 'pixeltype.ttf')
image_path = os.path.join(BASE_PATH, 'graphics')

# Define your game settings and variables here
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1200

game_active = True
scroll_sky = 0
scroll_ground = 0
player_score = 0
snail_y = 310
snail1_speed = 3
snail2_speed = 2
moving_left = False
moving_right = False
is_midair = False
scored_snail1 = False
scored_snail2 = False

pygame.init()
clock = pygame.time.Clock()
test_font = pygame.font.Font(font_path, 50)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
sky_surface = pygame.image.load(os.path.join(image_path, 'sky.png')).convert()
ground_surface = pygame.image.load(os.path.join(image_path, 'ground.png')).convert()
score_surf = test_font.render("SCORE: " + str(player_score), False, 'White')
end_surf = test_font.render('Game Over', False, 'White')
end_continue_surf = test_font.render('Press SPACE to continue', False, 'White')
end_exit_surf = test_font.render('Press ESCAPE to exit', False, 'White')

score_rect = score_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50))
snail1_surface = pygame.image.load(os.path.join(image_path, 'snail/snail1.png')).convert_alpha()
snail1_rect = snail1_surface.get_rect(midbottom=(SCREEN_WIDTH, snail_y))

snail2_surface = pygame.image.load(os.path.join(image_path, 'snail/snail2.png')).convert_alpha()
snail2_rect = snail2_surface.get_rect(midbottom=(SCREEN_WIDTH, snail_y))

player_surface = pygame.image.load(os.path.join(image_path, 'player/player_walk_1.png')).convert_alpha()
player_rect = player_surface.get_rect(midbottom=(50, 310))
player_gravity = 0

sky_width = sky_surface.get_width()
ground_width = ground_surface.get_width()
tiles = math.ceil(SCREEN_WIDTH / sky_width) + 1

