from typing import Any
import pygame, sys
import math

pygame.init()
WIDTH, HEIGHT = 800,600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class InverseKinematic():
    def __init__(self, start_node, num_segs, length=10):
        self.segments = []
        for i in range(num_segs):
            x, y = start_node
            segment = Segment(start_node, (x+length, y), length, 0)
            self.segments.append(segment)
            start_node = (x+length, y)
    def update(self):
        for i in self.segments:
            i.

        

class Segment(pygame.sprite.Sprite):
    def __init__(self, start_node, end_node, length, angle):
        self.start_node = pygame.Vector2(start_node)
        self.end_node = pygame.Vector2(end_node)
        self.angle = 0
        self.length = length
        self.width = 10

    def calculate_end_point(self):
        x, y = self.start_node
        dx = self.length*math.cos(self.angle)
        dy = self.length*math.sin(self.angle)
        self.end_node.x = x+dx
        self.end_node.y = y+dy

    def calculate_start_point(self, target):
        dx = self.length * math.cos(self.angle)
        dy = self.length * math.sin(self.angle)
        self.start_node.x = target[0]-dx
        self.start_node.y = target[1]-dy

    def update(self):
        self.calculate_end_point()
        self.draw()

    def follow(self, target):
        _, angle = trig(self.start_node, target)
        self.angle = angle
        self.calculate_start_point(target)


    def draw(self):
        pygame.draw.line(screen, (255, 255, 255), self.start_node, self.end_node, width=self.width)

def trig(e1, e2):
    dx = e2[0] - e1[0]
    dy = e2[1] - e1[1]
    distance = math.hypot(dx, dy)
    angle = math.atan2(dy, dx)
    return distance, angle

s = Segment((50,50), (300,200), 100, 10)
s2 = Segment((150,50), (300,200), 100, 10)

while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    s.follow(pygame.mouse.get_pos())
    s.update()
    s2.follow(s.start_node)
    s2.update()


    pygame.display.update()