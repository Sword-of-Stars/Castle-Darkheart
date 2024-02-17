import pygame, sys
import math

WIDTH, HEIGHT = 800,600

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Dancer():
    def __init__(self, x, y):
        self.rect = pygame.rect.Rect(x,y,20,20)

length = 150
k = 7

t = 0
center = [WIDTH//2, HEIGHT//2]

dancers = []
for i in range(0, k):
    dancer = [[center[0] + math.cos(2*math.pi/k*i)*length, center[1] + math.sin(2*math.pi/k*i)*length], math.pi/k*i, 0, math.pi]
    dancers.append(dancer)

dt = .01

while True:
    clock.tick(60)
    screen.fill((0,0,0))

    t += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update dancers
    for i, dancer in enumerate(dancers):
        dancer[1] = (dancer[1]+dt)%(2*math.pi)
        dancer[0] = [center[0] + math.sin(k*dancer[1])*math.cos(dancer[1])*length, 
                     center[1] + math.sin(k*dancer[1])*math.sin(dancer[1])*length]
        dancer[2] = (dancer[2]+((i%2)*-1)*dt*6)%(2*math.pi)
        dancer[3] = (dancer[3]+((i%2)*-1)*dt*6)%(2*math.pi)




    pygame.draw.circle(screen, (255,0,0), center, 10)

    for dancer in dancers:
        pygame.draw.circle(screen, (0,0,255), dancer[0], 10)
        pygame.draw.circle(screen, (0,255,255), [dancer[0][0] + math.cos(dancer[2])*20, 
                                                dancer[0][1] + math.sin(dancer[2])*20], 5)
        pygame.draw.circle(screen, (0,255,255), [dancer[0][0] + math.cos(dancer[3])*20, 
                                                dancer[0][1] + math.sin(dancer[3])*20], 5)




    pygame.display.flip()