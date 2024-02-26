import math
import pygame, sys

pygame.init()

screen = pygame.display.set_mode((500,500))

class Circle():
    def __init__(self, pos, radius, color=(255,0,0)):
        self.pos = pygame.Vector2(pos)
        self.radius = radius

        self.color = color
    
    def draw(self):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)

def distance(e1, e2):
    dx = e2[0]-e1[0]
    dy = e2[1]-e1[1]
    return math.hypot(dx, dy)

def angle_to(e1, e2):
    """Returns the angle from e1 to e2

    Arg:
        e1, e2 (seq): x-y coordinates
    Returns:
        float: angle in degrees
    """

    dx = e2[0]-e1[0]
    dy = e2[1]-e1[1]
    angle = math.atan2(dy,dx)
   
    return angle

def polar_to_point(pos, angle, dist):
    x = pos[0] + math.cos(angle)*dist
    y = pos[1] + math.sin(angle)*dist
    return pygame.Vector2(x,y)

def calculate_internal_bitangents(c1, c2):
    dist =  distance(c1.pos, c2.pos)
    a1 = angle_to(c1.pos, c2.pos)
    a2 = angle_to(c2.pos, c1.pos)
    if dist > (c1.radius+c2.radius):
        theta = math.acos((c1.radius+c2.radius)/dist)

        p1 = polar_to_point(c1.pos, a1+theta, c1.radius)
        p2 = polar_to_point(c1.pos, a1-theta, c1.radius)
        p3 = polar_to_point(c2.pos, a2+theta, c2.radius)
        p4 = polar_to_point(c2.pos, a2-theta, c2.radius)

        pygame.draw.line(screen, (0,0,255), p1, p3, width=5)
        pygame.draw.line(screen, (0,0,255), p2, p4, width=5)


        return [[p1, p2], [p3, p4]]
    
    return []

def calculate_external_bitangents(c1, c2):
    c1, c2 = sorted([c1, c2], key=lambda x: -x.radius)
    dist =  distance(c1.pos, c2.pos)
    a1 = angle_to(c1.pos, c2.pos)
    if dist > abs(c1.radius-c2.radius):
        theta = math.acos(abs(c1.radius-c2.radius)/dist)

        p1 = polar_to_point(c1.pos, a1+theta, c1.radius)
        p2 = polar_to_point(c1.pos, a1-theta, c1.radius)
        p3 = polar_to_point(c2.pos, a1+theta, c2.radius)
        p4 = polar_to_point(c2.pos, a1-theta, c2.radius)

        pygame.draw.line(screen, (0,0,255), p1, p3, width=5)
        pygame.draw.line(screen, (0,0,255), p2, p4, width=5)

        return [[p1, p2], [p3, p4]]
    
    return []

def line_of_sight(p, l1, l2):
    u = (p-l1).dot(l2-l1)/(l2-l1).dot(l2-l1)
    e = l1+min(max(0, u), 1)*(l2-l1)    
    dist = (e-p).magnitude()

c1 = Circle((250,250),30)
c2 = Circle((250,250),30, color=(0,255,0))

l1, l2 = pygame.Vector2(10,10), pygame.Vector2(150,150)
p = pygame.Vector2(100,160)

circles = [c1, c2]

    # Main loop
while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEWHEEL:
            c2.radius = max(10, c2.radius+event.y)

    c2.pos = pygame.mouse.get_pos()
    for circle in circles:
        circle.draw()

    calculate_internal_bitangents(c1, c2)
    calculate_external_bitangents(c1, c2)

    line_of_sight(p, l1, l2)


    pygame.display.flip()
