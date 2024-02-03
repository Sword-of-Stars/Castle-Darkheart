import pygame, sys

from scripts.entities.player import Player
from scripts.rendering.camera import Camera
from scripts.utils.mapreader import Map
from scripts.data_structures.tile_database import Database
from scripts.rendering.animation import anim_handler
from scripts.entities.projectile import proj_handler

from scripts.entities.enemy import Wendigo

from scripts.utils.handle_events import handle_events
from scripts.utils.core_functions import circle_collide

# TODO: Move all animations to a centralized animation controller
# TODO: Never blit things to screen, blit to camera for z-ordering and then shaders, then screen
# TODO: Fix player idle/walk cycle animations, something's out of sync

#===== Pygame Initialization =====#
pygame.init()
WIDTH, HEIGHT = 1200,800
screen = pygame.display.set_mode((WIDTH, HEIGHT),  pygame.OPENGL | pygame.DOUBLEBUF)
camera = Camera(0,0,WIDTH, HEIGHT)
clock = pygame.time.Clock()
font = pygame.font.SysFont('ErasITC', 20)

#===== Object Creation =====#
player = Player(1000, 1000)

#wendigo = Wendigo(1000, 1000)

db = Database()
world = Map("maps/done2", db, camera)

#===== Main Game Loop =====#
while True:
    clock.tick(60)
    camera.fill()

    pygame.display.set_caption(str(player.state))#str(clock.get_fps()))

    handle_events(player)
    
    

    pos = pygame.mouse.get_pos()
    player.update(world.obstacles, camera, pos)

    dx, dy = camera.move(player)

    for obstacle in world.obstacles:
        obstacle.update(camera)
    
    for asset in world.assets:
        asset.update(camera)

    world.draw_world(camera)

    # Send to external function
    player.move_camera(camera, dx, dy)
    #wendigo.move_camera(camera, dx, dy)

    # send to external function
    anim_handler.update(camera)
    proj_handler.update(camera)

    #for proj in proj_handler.projectile_list:
        #if circle_collide(proj.pos, proj.radius, wendigo.rect.center, wendigo.radius):
            #wendigo.take_hit(proj)

    #wendigo.update(camera, player, world.obstacles)

    #pygame.draw.circle(camera.display, (255, 0,0), (100,100), 20)

    camera.draw_world()
    camera.update()