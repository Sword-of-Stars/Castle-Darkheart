# TODO:
# 1) Add some acceleration, get feedback on game feel
# 2) Implement a camera system, with screen inside of camera

# NOTE:
# 1) I should use WASD for my controls, as keyboard jamming/ghosting limits the number of simultaneous arrow key readings
# 2) Fixed initial bug with player glitching through obstacles, can no longer replicate
# 3) Cannot have overlapping obstacles, leads to glitches

import pygame, sys

from scripts.obstacle import Obstacle
from scripts.player2 import Player
from scripts.camera import Camera

from scripts.handle_events2 import handle_events

pygame.init()
WIDTH, HEIGHT = 1200,800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
camera = Camera(0,0,WIDTH, HEIGHT)
clock = pygame.time.Clock()
font = pygame.font.SysFont('ErasITC', 20)

# Objects #
player = Player(100, 100)
obstacles = [Obstacle(440, 300), Obstacle(240, 100)]

while True:
    clock.tick(60)
    camera.fill()

    handle_events(player)
    
    for obstacle in obstacles:
        obstacle.update(camera)

    pos = pygame.mouse.get_pos()
    player.update(obstacles, camera, pos)

    camera.move(player)
    camera.update(screen)

    pygame.display.update()