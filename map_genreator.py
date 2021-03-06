import pygame
import random
import numpy
from map_objects_and_tiles import *
from screen_settings import *

'''
This file contains all the code and functions that generates a new random map when
starting the game or by pressing the "M" button.
'''

Vector2 = pygame.math.Vector2
map_image = pygame.Surface((screen_width, screen_height))

wall_list = []
grav_well_list = []
laser_list = []
win_tile_list = []

''' Main function that goes through different processes in order to create a new random map for the player to explore'''


def generate_a_map():
    pos_x = 0
    pos_y = 0

    # This is what creates the map matrix array by using the numpy.random function from the numpy library
    map_matrix = numpy.random.randint(6, size=(screen_height / 64, screen_width / 64))
    player_spawn = False
    win_tile = False

    generate_a_map.list_of_wall_pos = []
    generate_a_map.list_of_grav_well_pos = []
    generate_a_map.list_of_laser_pos = []
    generate_a_map.list_of_win_tile_pos = []

    generate_a_map.player_spawn_pos = (0, 0)

    # This for loop goes through each number in the map matrix array and applies rules to it
    for row_num, row_list in enumerate(map_matrix):
        for tile_num in enumerate(row_list):

            # gets the position of the tile above and the tile to the left
            tile_left = (row_num, tile_num[0] - 1)
            current_pos = (row_num, tile_num[0])

            # IF statement rules to apply to the map matrix
            # These IF statements is what makes the random map look a certain way

            # This IF statement creates wall all around the map
            if row_num == 0 or row_num == screen_height / 64 - 1 or tile_num[0] == 0 \
                    or tile_num[0] == screen_width / 64 - 1:
                map_matrix.itemset(current_pos, 1)

            elif random.random() < 0.3 and map_matrix.item(tile_left) == 1:
                map_matrix.itemset(current_pos, 1)

            elif random.random() < 0.5 and tile_num[1] == 3:
                map_matrix.itemset(current_pos, 0)

            elif random.random() < 0.75 and tile_num[1] == 4:
                map_matrix.itemset(current_pos, 0)

            elif random.random() < 0.6 or (player_spawn and tile_num[1] == 2):
                map_matrix.itemset(current_pos, 0)

            elif tile_num[1] == 5 and not win_tile:
                map_matrix.itemset(current_pos, 5)
                win_tile = True

            elif tile_num[1] == 5 and win_tile:
                map_matrix.itemset(current_pos, 0)

            elif random.random() < 0.1:
                map_matrix.itemset(current_pos, 4)

            elif random.random() < 0.3 and not player_spawn:
                map_matrix.itemset(current_pos, 2)
                player_spawn = True

    print map_matrix

    # These lists need to be deleted before creating a new map so the old colliders don't stick around
    del wall_list[:]
    del grav_well_list[:]
    del laser_list[:]
    del win_tile_list[:]

    '''Creates the map image from the map matrix by checking each number
    in the matrix array and blitting the equivalent tile image to map position'''

    for row_num, row_list in enumerate(map_matrix):
        for tile_num in enumerate(row_list):
            floor = Floor(pos_x, pos_y)
            player_tile = PlayerSpawnTile(pos_x, pos_y)

            # render all images made in map objects and tiles
            if tile_num[1] == 1:
                generate_a_map.wall_pos = (pos_x, pos_y)
                wall = Wall(generate_a_map.wall_pos)
                wall.render(map_image)
                generate_a_map.list_of_wall_pos.append(generate_a_map.wall_pos)
                wall_list.append(wall)

            elif tile_num[1] == 2:
                player_tile.render(map_image)
                generate_a_map.player_spawn_pos = (pos_x, pos_y)

            elif tile_num[1] == 3:
                generate_a_map.grav_well_pos = (pos_x, pos_y)
                grav_well = GravWell(generate_a_map.grav_well_pos)
                grav_well.render(map_image)
                generate_a_map.list_of_grav_well_pos.append(generate_a_map.grav_well_pos)
                grav_well_list.append(grav_well)

            elif tile_num[1] == 4:
                generate_a_map.laser_pos = (pos_x, pos_y)
                laser = Laser(generate_a_map.laser_pos)
                floor.render(map_image)
                generate_a_map.list_of_laser_pos.append(generate_a_map.laser_pos)
                laser_list.append(laser)

            elif tile_num[1] == 5:
                generate_a_map.win_tile_pos = (pos_x, pos_y)
                win_tile = PlayerWinTile(generate_a_map.win_tile_pos)
                win_tile.render(map_image)
                generate_a_map.list_of_win_tile_pos.append(generate_a_map.win_tile_pos)
                win_tile_list.append(win_tile)

            elif tile_num[1] == 0:
                floor.render(map_image)

            pos_x += 64
        pos_y += 64
        pos_x = 0


# function to render the map image to the screen, this gets called in the main
def render_map():
    screen.blit(map_image, (0, 0))


# function to render the lasers on the map, this gets called in player_class
def render_lasers():
    for laser in laser_list:
        laser.update(screen)
