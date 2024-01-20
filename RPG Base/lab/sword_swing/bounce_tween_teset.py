import pygame, sys
import pytweening

pygame.init()
WIDTH, HEIGHT = 800,600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

surf = pygame.surface.Surface((100,100))
pygame.draw.circle(surf, (255, 0, 0), (50,50), 50)

t = 0.01
direction = 1

while True:
    clock.tick(60)
    screen.fill((0,0,0))

    t += 0.01*direction
    if t >= 1:
        t = 1
        direction *= -1

    elif t<= 0:
        t = 0
        direction *= -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    new_surf = pygame.transform.scale_by(surf, (1+pytweening.easeInElastic(t),1+2*pytweening.easeInElastic(t)))
    screen.blit(new_surf, (100,100))


    pygame.display.update()