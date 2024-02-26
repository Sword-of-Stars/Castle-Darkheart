import pygame, sys

from scripts.entities.player import Player
from scripts.rendering.camera import Camera
from scripts.utils.mapreader import Map
from scripts.data_structures.tile_database import Database
from scripts.entities.HUD import HUD

from scripts.rendering.animation import anim_handler
from scripts.entities.projectile import proj_handler
from scripts.vfx.particles import part_handler
from scripts.entities.enemy import Wendigo, enemy_handler


from scripts.utils.handle_events import handle_events
from scripts.utils.handle_projectiles import handle_projectiles


#===== Pygame Initialization =====#
pygame.init()

from scripts.story.text_box import TextBox
from scripts.story.story_manager import StoryManager


WIDTH, HEIGHT = 1200,800
screen = pygame.display.set_mode((WIDTH, HEIGHT),  pygame.OPENGL | pygame.DOUBLEBUF | pygame.HIDDEN)
camera = Camera(0,0,WIDTH, HEIGHT)
clock = pygame.time.Clock()
font = pygame.font.SysFont('ErasITC', 20)

#===== Mixer Initialization =====#
pygame.mixer.init()
pygame.mixer.music.load('data/music/backing-1/walking_music.mp3')
#pygame.mixer.music.play(-1)

#===== Object Creation =====#
player = Player(1300, 0)

Wendigo(0, 100)
Wendigo(100, 100)
Wendigo(100, 150)
Wendigo(300, 130)
#Wendigo(200, 100)
#Wendigo(20, 100)


hud = HUD(player, camera)

db = Database()

world = Map("maps/floor_swap", db, camera)
world.load_map(camera)


ggg = TextBox("The Book of Kemmler", "In Xanadu did Kublai Khan\nA ststely pleasure dome decree\nWherealphthesacredrierran \nthru cavernes measureless to man\ndown to a sunless se")
sm = StoryManager()

#===== Main Game Loop =====#
screen = pygame.display.set_mode((WIDTH, HEIGHT),  pygame.OPENGL | pygame.DOUBLEBUF)

while True:
    clock.tick(60)
    camera.fill()

    pygame.display.set_caption(str(clock.get_fps()))
    #pygame.display.set_caption(f"{camera.x}, {camera.y}")


    handle_events(player, ggg)
    
    pos = pygame.mouse.get_pos()
    player.update(world.obstacles, camera, pos)

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

    #ggg.update(camera)

    world.draw_world(camera)

    # Send to external function
    player.move_camera(camera, dx, dy)

    # send to external function
    anim_handler.update(camera)
    proj_handler.update(camera, dx, dy, world.obstacles)

    handle_projectiles(proj_handler, enemy_handler, player, part_handler)

    enemy_handler.update(camera, dx, dy, world.obstacles, player)

    sm.update_triggers(world.triggers, player)
    
    camera.draw_world()
    camera.update()