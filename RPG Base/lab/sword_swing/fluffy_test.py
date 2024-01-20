# Setup Python ----------------------------------------------- #
import pygame, sys
 
# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((500, 500),0,32)
 
# make sure you provide your own image
#img = pygame.image.load('pic.png').convert()
img = pygame.surface.Surface((100,100))
pygame.draw.rect(img, (255, 255, 0), (0,0,100,100))
img.set_colorkey((0,0,0))

def blitRotateCenter(surf, image, topleft, angle):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = topleft).center)

    surf.blit(rotated_image, new_rect)
 
angle = 0
# Loop ------------------------------------------------------- #
while True:
    angle += 6

    pygame.display.set_caption(f"FPS: {mainClock.get_fps()}")

    
    # Background --------------------------------------------- #
    screen.fill((0,50,0))
 
    mx, my = pygame.mouse.get_pos()
    blitRotateCenter(screen, img, (mx,my), angle)

    # Buttons ------------------------------------------------ #
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
                
    # Update ------------------------------------------------- #
    pygame.display.update()
    mainClock.tick(0)