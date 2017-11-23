import pygame
from screen_settings import *
from player_class import *
from map_genreator import *
import time
# initiate pygame
pygame.init()

# limiting the FPS with this fps clock
FPS = 60
fpsClock = pygame.time.Clock()


generate_a_map()
player = Player(generate_a_map.player_spawn_pos)

toggle_state = False

running = True
time1= 0.00
while running:
    time2=time1
    time1=time.clock()
    deltatime = time1-time2
    pressed_keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            generate_a_map()

        # toggle between vision
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            toggle_state = not toggle_state


    if not toggle_state:
        player.vision_mechanic(deltatime)
    else:
        render_map()
        render_lasers()

    # running core gameplay elements

    player.render(screen)
    player.player_movement(wall_list, grav_well_list, laser_list, win_tile_list)

    pygame.display.update()
    fpsClock.tick(FPS)