import pygame, sys, random, math

BASE_PATH = 'C:/Users/Kitsa/OneDrive/Desktop/pyrunner/pygame_runner'
font_path = BASE_PATH + '/fonts/pixeltype.ttf'
image_path = BASE_PATH + '/graphics/'
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1200

game_active = True
scroll_sky = 0
scroll_ground = 0
snail_y = 310
snail1_speed = 3
snail2_speed = 2
# Initialize movement variables
moving_left = False
moving_right = False
is_midair = False

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)) #width,height
pygame.display.set_caption('Test Game')
clock = pygame.time.Clock()
test_font = pygame.font.Font(font_path, 50)

sky_surface = pygame.image.load(image_path + 'sky.png').convert()
ground_surface = pygame.image.load(image_path + 'ground.png').convert()
score_surf = test_font.render('HELLO BIG BOYS', False, 'White')
end_surf = test_font.render('Game Over', False, 'White')
end_continue_surf = test_font.render('Press SPACE to continue', False, 'White')
end_exit_surf = test_font.render('Press ESCAPE to exit', False, 'White')

score_rect = score_surf.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT-50))
snail1_surface = pygame.image.load(image_path + 'snail/snail1.png').convert_alpha()
snail1_rect = snail1_surface.get_rect(midbottom = (SCREEN_WIDTH, snail_y))

snail2_surface = pygame.image.load(image_path + 'snail/snail2.png').convert_alpha()
snail2_rect = snail2_surface.get_rect(midbottom = (SCREEN_WIDTH, snail_y))

player_surface = pygame.image.load(image_path + 'player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom=(50, 310))
player_gravity = 0

sky_width = sky_surface.get_width()
ground_width = ground_surface.get_width()
tiles = math.ceil(SCREEN_WIDTH/sky_width) + 1


while True:

    #exit loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Jump if spacekey down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_midair:
                player_gravity = -20
                is_midair = True

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
        #draw background
        for i in range(0, tiles):
            screen.blit(sky_surface, (i * sky_width + scroll_sky, 0))
        for i in range(0, tiles):
            screen.blit(ground_surface, (i * ground_width + scroll_ground, 310))

        #scroll background
        scroll_sky -= 0.25
        scroll_ground -= 1

        #reset scroll
        if abs(scroll_sky) > sky_width:
            scroll_sky = 0
        if abs(scroll_ground) > ground_width:
            scroll_ground = 0

        #draw snails
        screen.blit(snail1_surface, snail1_rect)
        screen.blit(snail2_surface, snail2_rect)

        #draw player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 310:
            player_rect.bottom = 310
        screen.blit(player_surface, player_rect)

        #draw text
        screen.blit(score_surf, score_rect)

        #moves the rect
        snail1_rect.x -= snail1_speed
        snail2_rect.x -= snail2_speed

        if snail1_rect.right <= 0:
            snail1_rect.left = SCREEN_WIDTH
            snail1_speed = random.randint(3, 8)

        if snail2_rect.right <= 0:
            snail2_rect.left = SCREEN_WIDTH
            snail2_speed = random.randint(3, 8)

        if snail1_rect.colliderect(player_rect) or snail2_rect.colliderect(player_rect):
            game_active = False
    else:
        #screen.fill('Black')
        screen.blit(score_surf, score_rect)
        screen.blit(end_surf, (400, 200))
        screen.blit(end_continue_surf, (400, 230))
        screen.blit(end_exit_surf, (400, 260))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            elif event.key == pygame.K_SPACE:
                game_active = True

    pygame.display.update()
    clock.tick(60) #should not run faster than 60 fps / max fps