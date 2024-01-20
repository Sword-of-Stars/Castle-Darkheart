import pygame, sys
import math, random

# Maybe I need to redo this using children rather than parents
# LOOK AT: https://www.alanzucconi.com/2017/04/10/gradient-descent/

pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Inverse Kinematics")
clock = pygame.time.Clock()

class Segment():
    def __init__(self, length, angle, angle_bound, prev, start_pos=None, end=False):

        self.angle = angle
        self.orig_angle = angle #Need to update later
        if start_pos != None: # If this is the first segment of the leg
            self.A = start_pos
            self.start_pos = start_pos
        else:
            self.A = prev.B
        self.length = length
        self.calculate_B()
        
        self.prev = prev
        if prev == None: self.delta_pos = [0,0]
        else: self.prev.next = self
        if end: self.next = None

        self.color = (255, 255, 255)


    def calculate_B(self):
        dx = self.length * math.cos(self.angle)
        dy = self.length * math.sin(self.angle)
        self.B = [self.A[0]+dx, self.A[1]+dy]

    def calculate_A(self, pos):
        dx = self.length * math.cos(self.angle)
        dy = self.length * math.sin(self.angle)

        self.A = [pos[0]-dx, pos[1]-dy]

        if self.prev == None:
            self.delta_pos = subtract_list(self.A, self.start_pos)
        
    def follow(self, pos):
        _, angle = trig(self.A, pos)
        '''if self.prev == None:
            self.angle = bound_angle(angle, math.pi/2, [math.pi/4, math.pi/4])
        else:
            self.angle = bound_angle(angle, self.prev.angle, [math.pi/1.5, math.pi/1.5])'''
        self.angle = angle
        self.calculate_A(pos)
    
    def draw(self):
        pygame.draw.line(screen, self.color, self.A, self.B, width=10)

    def update(self, pos=None):
        if self.next == None:
            self.follow(pos)
        else:
            self.follow(self.next.A)

        self.calculate_B()

        if self.prev != None:
            self.prev.update(pos)

    def lock_point(self, delta_pos=None):
        if self.prev == None:
            delta_pos = self.delta_pos

        self.A = subtract_list(self.A, delta_pos)
        self.B = subtract_list(self.B, delta_pos)
        
        self.draw()

        if self.next != None:
            self.next.lock_point(delta_pos)


class IKLeg():
    def __init__(self, num_segs, length):
        self.build_forward(num_segs, length)

    def build_forward(self, num_segs, length):
        self.root = Segment(length, 0, None, prev=None, start_pos=(300,300), end=False)
        prev = self.root
        for i in range(num_segs-1):
            end = (i==num_segs-2)
            prev = Segment(length, 0, None, prev, start_pos=None, end=end)
        self.tail = prev

    def update(self, pos):
        self.tail.update(pos=pos)
        self.root.lock_point()

ball_pos = [0,HEIGHT//2]
ball_speed = 5

def trig(e1, e2):
    dx = e2[0] - e1[0]
    dy = e2[1] - e1[1]
    distance = math.hypot(dx, dy)
    angle = math.atan2(dy, dx)
    return distance, angle

def bound_angle(angle, anchor, bounds):
    # assuming radian input
    left_bound = anchor-bounds[0]
    right_bound = anchor+bounds[1]

    #if angle < 0: #Temp fix, not lasting
        #angle *= -1

    angle = angle%(2*math.pi)

    if angle < left_bound:
        angle_to_return = left_bound
    elif angle > right_bound:
        angle_to_return = right_bound
    else:
        angle_to_return = angle

    return angle_to_return%(2*math.pi)

def subtract_list(a, b):
    return [x - y for x, y in zip(a, b)]

leg1 = IKLeg(2, 100)
leg2 = IKLeg(5, 60)
leg1.root.start_pos = [300,HEIGHT]
leg2.root.start_pos = [300,0]
legs = [leg1, leg2]

while True:
    screen.fill((0,0,0))
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pos = pygame.mouse.get_pos()

    ball_pos[0] += ball_speed
    pygame.draw.circle(screen, (255, 0, 0), ball_pos, 30)
    if ball_pos[0] > WIDTH or ball_pos[0] < 0:
        ball_speed *= -1

    for leg in legs:
        leg.update(ball_pos)

    pygame.display.update()