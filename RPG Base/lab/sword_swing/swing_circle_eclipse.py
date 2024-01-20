import pygame, sys
import math

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.init()

def angle_to(e1, e2):
    dx = e2[0]-e1[0]
    dy = e2[1]-e1[1]
    return math.degrees(math.atan2(dy,dx))

def draw_circle():
    subsurf = pygame.surface.Surface((80,40))
    subsurf.fill((0,0,0))
    pygame.draw.circle(subsurf, (255, 255, 255), (20,20), 20)
    pygame.draw.circle(subsurf, (0,0,0), (32,20), 20)
    subsurf = pygame.transform.scale_by(subsurf, (2,1)) # ALl I need to do is come up with some fancy maths
        # To offset the scaling in a trigonometric way and voila!, it is completed. 
    subsurf.set_colorkey((0,0,0))
    #subsurf = pygame.transform.scale_by()
    return subsurf


class Player():
    def __init__(self):
        self.pos = (WIDTH//2, HEIGHT//2)
        self.color = (0,0,255)
        self.radius = 30

    def update(self):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)

player = Player()
surf = draw_circle()

while True:
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    player.update()

    pos = pygame.mouse.get_pos()
    pygame.draw.circle(screen, (255, 0,0), pos, 10)

    pygame.display.set_caption(str(angle_to(player.pos, pos)))

    screen.blit(surf, (50,50))

    pygame.display.update()