import pygame, sys

from scripts.entities.player import Player
from scripts.rendering.camera import Camera
from scripts.utils.mapreader import Map
from scripts.data_structures.tile_database import Database
from scripts.entities.HUD import HUD
from scripts.ui.mouse import Mouse

from scripts.rendering.animation import anim_handler
from scripts.entities.projectile import proj_handler
from scripts.vfx.particles import part_handler
from scripts.entities.enemy import Wendigo, enemy_handler


from scripts.utils.handle_events import handle_events
from scripts.utils.handle_projectiles import handle_projectiles 

from scripts.ui.tutorial import Tutorial


def main(state):
    clock.tick(60)
    camera.fill()

    camera.vignette = 0.55

    pygame.display.set_caption(str(clock.get_fps()))

    handle_events(player, tutorial)

    pos = pygame.mouse.get_pos()
    state = player.update(world.obstacles, camera, pos)

    dx, dy = camera.move(player)

    part_handler.update(camera, dx, dy, world.obstacles)

    #==== Update the World ====#
    for obstacle in world.obstacles:
        obstacle.update(camera)
    for asset in world.assets:
        asset.update(camera)
    for trigger in world.triggers:
        trigger.update(camera)

    hud.update()

    world.draw_world(camera)

    # Send to external function
    player.move_camera(camera, dx, dy)

    # send to external function
    anim_handler.update(camera)
    proj_handler.update(camera, dx, dy, world.obstacles)

    handle_projectiles(proj_handler, enemy_handler, player, part_handler)

    enemy_handler.update(camera, dx, dy, world.obstacles, player)

    tutorial.update(camera)
    mouse.update(camera)


    camera.draw_world()
    camera.update()

    if state != "game":
        enemy_handler.enemy_list = []

    return state


WIDTH, HEIGHT = 1920,1080
screen = pygame.display.set_mode((WIDTH, HEIGHT),  pygame.OPENGL | pygame.DOUBLEBUF | pygame.HIDDEN)
camera = Camera(0,0,WIDTH, HEIGHT)
clock = pygame.time.Clock()
font = pygame.font.SysFont('ErasITC', 20)


player = Player(0, 0)

def reset():
    player.reset(0, 0)
    for i in range(6):
        Wendigo(0, -2000+100-60*i)

    camera.reset()

reset()
    

hud = HUD(player, camera)
db = Database()

world = Map("maps/xander_swap", db, camera)
world.load_map(camera)

mouse = Mouse()

tutorial = Tutorial(camera, True)