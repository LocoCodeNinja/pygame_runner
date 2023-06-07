import pygame, sys, random, math

BASE_PATH = 'C:/Users/Kitsa/OneDrive/Desktop/pyrunner/pygame_runner'
font_path = BASE_PATH + '/fonts/pixeltype.ttf'
image_path = BASE_PATH + '/graphics/'
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1200
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)) #width,height
pygame.display.set_caption('Test Game')
clock = pygame.time.Clock()
test_font = pygame.font.Font(font_path, 50)

sky_surface = pygame.image.load(image_path + 'sky.png').convert()
ground_surface = pygame.image.load(image_path + 'ground.png').convert()
text_surface = test_font.render('HELLO', False, 'White')
snail1_surface = pygame.image.load(image_path + 'snail/snail1.png').convert_alpha()
snail2_surface = pygame.image.load(image_path + 'snail/snail2.png').convert_alpha()
player_surface = pygame.image.load(image_path + 'player/player_walk_1.png').convert_alpha()


sky_width = sky_surface.get_width()
ground_width = ground_surface.get_width()
tiles = math.ceil(SCREEN_WIDTH/sky_width) + 1
scroll_sky = 0
scroll_ground = 0
snail1_x = SCREEN_WIDTH
snail2_x = SCREEN_WIDTH
snail_y = 280
snail1_speed = 3
snail2_speed = 2

while True:

    #exit loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

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
    screen.blit(snail1_surface, (snail1_x,snail_y))
    screen.blit(snail2_surface, (snail2_x,snail_y))

    #draw player
    screen.blit(player_surface, (20, 235))

    #draw text
    screen.blit(text_surface, (300,50))

    snail1_x -= snail1_speed
    snail2_x -= snail2_speed

    if snail1_x < -100:
        snail1_x = SCREEN_WIDTH
        snail1_speed = random.randint(2, 6)

    if snail2_x < -100:
        snail2_x = SCREEN_WIDTH
        snail2_speed = random.randint(2, 6)

    pygame.display.update()
    clock.tick(60) #should not run faster than 60 fps / max fps