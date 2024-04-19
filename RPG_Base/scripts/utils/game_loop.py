import pygame, sys
import random, math

from scripts.entities.player import Player
from scripts.rendering.camera import Camera
from scripts.utils.mapreader import Map
from scripts.data_structures.tile_database import Database
from scripts.entities.HUD import HUD
from scripts.ui.mouse import Mouse
from scripts.entities.dancers import Dancer, generate_rose

from scripts.rendering.animation import anim_handler
from scripts.entities.projectile import proj_handler
from scripts.vfx.particles import part_handler
from scripts.entities.enemy import Wendigo, enemy_handler


from scripts.utils.handle_events import handle_events
from scripts.utils.handle_projectiles import handle_projectiles 

from scripts.ui.tutorial import Tutorial
from scripts.story.text_box import TextBox

def main(state):
    global track, spawn_timer, dancers, win, alpha
    
    if spawn_timer > 0 and len(enemy_handler.enemy_list) < 3:
        spawn_timer -= 1

    clock.tick(60)
    camera.fill()

    camera.vignette = 0.55

    hud.update()

    txt = None
    for altar in world.altars:
        altar.is_over(mouse)
        altar.update(camera)

        if altar.clicked and player.is_alive:
            txt = altar.txt

        if altar.final and player.num_altars >= 3:
            altar.is_near(player)
            if altar.found:
                win = True

    if txt != None:
        txt.update_msg()
        txt.update(camera)

        if txt.all_finished:
            txt = None
            altar.clicked = False
        


    handle_events(player, tutorial, txt, camera)

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

    threshold = -14300
    if camera.y < threshold: #13800

        if track == "back":
            track = "waltz"

            pygame.mixer.stop()
            pygame.mixer.music.load("data/music/waltz-1/waltz.mp3")
            pygame.mixer.music.play(-1)
        if not win:
            for dancer in dancers:
                dancer.move_camera(camera, dx, dy)
                dancer.update(camera)

                if dancer.rect.colliderect(player.rect):
                    player.take_damage(1, dancer)

    
    elif camera.y > threshold:
        if track == "waltz":
            track = "back"

            pygame.mixer.stop()
            pygame.mixer.music.load("data/music/backing-1/walking_music.mp3")
            pygame.mixer.music.play(-1)


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



    if not player.is_alive:
        tutorial.active = False
        txt = None

    player.num_altars = 0
    for altar in world.all_altars:
        if altar.found:
            player.num_altars += 1

    if state != "game":
        enemy_handler.enemy_list = []

    

    dist = 60
    if camera.y < -1000 and camera.y > threshold:
        if spawn_timer <= 0 and len(enemy_handler.enemy_list) < 3:
            spawn_timer = random.randint(300,1000)
            death_sound.play()

            for i in range(3):
                Wendigo(player.pos[0]+math.cos(2*math.pi/3*i)*dist, 
                        player.pos[1]+math.sin(2*math.pi/3*i)*dist-100)
    
    camera.draw_world()
     
    if win:
        surf = pygame.surface.Surface((WIDTH, HEIGHT))
        surf.fill((0,0,0))
        surf.set_alpha(alpha)
        
        camera.ui_surf.fill((0,0,0,0))
        alpha = min(255, alpha+1)
        camera.display.blit(surf, (0,0))

        if alpha >= 254:
            state = "credits"



    camera.update()

    

    return state, track


WIDTH, HEIGHT = 1600, 1024
print(pygame.display.list_modes())
screen = pygame.display.set_mode((WIDTH, HEIGHT),  pygame.OPENGL | pygame.DOUBLEBUF | pygame.HIDDEN)
camera = Camera(0,0,WIDTH, HEIGHT)
clock = pygame.time.Clock()
font = pygame.font.SysFont('ErasITC', 20)


player = Player(0,0)

global track, spawn_timer, dancers, win, alpha
track = "back"
spawn_timer = 0
win = False
alpha = 0


def reset():
    global dancers
    pygame.mixer.music.stop()
    pygame.mixer.music.load("data/music/backing-1/walking_music.mp3")
    pygame.mixer.music.play(-1)
    player.reset(0,0)

    center = (1307, -18581)
    dancers = generate_rose(300, 20, center) +  generate_rose(500, 5, center) + generate_rose(600, 7, center)
    

    camera.reset()

    

hud = HUD(player, camera)
db = Database()

world = Map("maps/final_map", db, camera)
world.load_map(camera)

mouse = Mouse()

tutorial = Tutorial(camera, True)
txt = None

death_sound = pygame.mixer.Sound("data/sound_effects/death_02.wav")
death_sound.set_volume(0.4)

dancers = []
#
