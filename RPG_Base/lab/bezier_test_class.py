"""
bezier.py - Calculates a bezier curve from control points. 
 
2007 Victor Blomqvist
Released to the Public Domain
"""
import pygame
from pygame.locals import *
 
gray = (100,100,100)
lightgray = (200,200,200)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
X,Y,Z = 0,1,2

class BezierCurve():
    def __init__(self, numPoints=None):
        self.control_points = [pygame.Vector2(100,100), pygame.Vector2(150,500), 
                                pygame.Vector2(450,500), pygame.Vector2(500,150)]
        self.vertices = [(x.x, x.y) for x in self.control_points]
        self.numPoints = 6
        self.bezier_points = self.compute_bezier_points()

    def compute_bezier_points(self):
        if self.numPoints is None:
            numPoints = 30
        elif self.numPoints <= 2 or len(self.vertices) != 4:
            return None

        result = []

        b0x = self.vertices[0][0]
        b0y = self.vertices[0][1]
        b1x = self.vertices[1][0]
        b1y = self.vertices[1][1]
        b2x = self.vertices[2][0]
        b2y = self.vertices[2][1]
        b3x = self.vertices[3][0]
        b3y = self.vertices[3][1]



        # Compute polynomial coefficients from Bezier points
        ax = -b0x + 3 * b1x + -3 * b2x + b3x
        ay = -b0y + 3 * b1y + -3 * b2y + b3y

        bx = 3 * b0x + -6 * b1x + 3 * b2x
        by = 3 * b0y + -6 * b1y + 3 * b2y

        cx = -3 * b0x + 3 * b1x
        cy = -3 * b0y + 3 * b1y

        dx = b0x
        dy = b0y

        # Set up the number of steps and step size
        numSteps = self.numPoints - 1 # arbitrary choice
        h = 1.0 / numSteps # compute our step size

        # Compute forward differences from Bezier points and "h"
        pointX = dx
        pointY = dy

        firstFDX = ax * (h * h * h) + bx * (h * h) + cx * h
        firstFDY = ay * (h * h * h) + by * (h * h) + cy * h


        secondFDX = 6 * ax * (h * h * h) + 2 * bx * (h * h)
        secondFDY = 6 * ay * (h * h * h) + 2 * by * (h * h)

        thirdFDX = 6 * ax * (h * h * h)
        thirdFDY = 6 * ay * (h * h * h)

        # Compute points at each step
        result.append((int(pointX), int(pointY)))

        for i in range(numSteps):
            pointX += firstFDX
            pointY += firstFDY

            firstFDX += secondFDX
            firstFDY += secondFDY

            secondFDX += thirdFDX
            secondFDY += thirdFDY

            result.append((int(pointX), int(pointY)))

        return result

    def update(self):
        for p in self.control_points:
            pygame.draw.circle(screen, blue, (int(p.x), int(p.y)), 4)

        self.vertices = [(x.x, x.y) for x in self.control_points]
        pygame.draw.lines(screen, lightgray, False, [(x.x, x.y) for x in self.control_points])
        b_points = self.compute_bezier_points()
        pygame.draw.lines(screen, pygame.Color("red"), False, b_points, 2)


def main():
    pygame.init()
    global screen
    screen = pygame.display.set_mode((1024, 768))

    curves = [BezierCurve() for i in range(2)]

    ### The currently selected point
    selected = None
    
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                running = False
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                for curve in curves:
                    for p in curve.control_points:
                        if abs(p.x - event.pos[X]) <= 10 and abs(p.y - event.pos[Y]) <= 10 :
                            selected = p
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                selected = None
        
        ### Draw stuff
        screen.fill(gray)
                
        if selected is not None:
            selected.x, selected.y = pygame.mouse.get_pos()
            pygame.draw.circle(screen, green, (selected.x, selected.y), 10)

        for curve in curves:
            curve.update()

        ### Flip screen
        pygame.display.flip()
        clock.tick(100)
        #print clock.get_fps()
    
if __name__ == '__main__':
    main()