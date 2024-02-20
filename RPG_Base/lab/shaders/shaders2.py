import pygame, sys, os
import moderngl
from numpy import array

os.chdir(f"{os.getcwd()}/lab/shaders")

pygame.init()

screen = pygame.display.set_mode((800,600))
ctx = moderngl.create_context()

clock = pygame.time.Clock()

img = pygame.image.load('lab/shaders/ti.jpg')

quad_buffer = ctx.buffer(data=array('f', [
    # position (x,y), uv coords (x,y)
    -1.0, 1.0, 0.0, 0.0,
    1.0, 1.0, 1.0, 0.0,
    -1.0, -1.0, 0.0, 1.0,
    1.0, -1.0, 1.0, 1.0
]))

while True:
    screen.fill((0,0,0))
    screen.blit(img, pygame.mouse.get_pos())

    pygame.display.set_caption(str(clock.get_fps()))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(60)