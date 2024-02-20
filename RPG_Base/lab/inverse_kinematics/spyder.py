import pygame, sys
import math, random

# Maybe I need to redo this using children rather than parents

pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Inverse Kinematics: Spider Demo")
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
        self.speed = 1.5


    def calculate_B(self):
        dx = self.length * math.cos(self.angle)
        dy = self.length * math.sin(self.angle)
        self.B = [self.A[0]+dx, self.A[1]+dy]

    def calculate_A(self, pos):
        dx = self.length * math.cos(self.angle)
        dy = self.length * math.sin(self.angle)

        if self.next == None:
            dist, angle = trig(self.A, [pos[0]-dx, pos[1]-dy])
            if dist > 6:
                print(f"too fast! {dist}")
                speed = 3
                self.A = [self.A[0]+speed*math.cos(angle), self.A[1]+speed*math.sin(angle)]
            else:
                self.A = [pos[0]-dx, pos[1]-dy]

        else:
            self.A = [pos[0]-dx, pos[1]-dy]

        if self.prev == None:
            self.delta_pos = subtract_list(self.A, self.start_pos)
        
    def follow(self, pos):
        _, angle = trig(self.A, pos)
        self.angle = angle

        #if self.prev == None:
            #self.angle = bound_angle(angle, 0, [math.pi/2, math.pi/2])
        #if self.next == None:
            #self.angle = bound_angle(angle, self.pre, [math.pi/2, math.pi/2])

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
    def __init__(self, num_segs, length, start_pos):
        self.build_forward(num_segs, length, start_pos)
        self.touching_target = False

        self.target = None
        self.previous_target = None
        self.speed = 10

    def build_forward(self, num_segs, length, start_pos):
        self.root = Segment(length, 0, None, prev=None, start_pos=start_pos, end=False)
        prev = self.root
        for i in range(num_segs-1):
            end = (i==num_segs-2)
            prev = Segment(length, 0, None, prev, start_pos=None, end=end)
        self.tail = prev
    
    def is_touching_target(self, delta_pos):
        x, y = delta_pos
        self.touching_target = (bound(x, 0, 3) and bound(y, 0, 3))

    def update(self, pos):
        self.tail.update(pos=pos)
        self.root.lock_point()
        self.is_touching_target(self.root.delta_pos)

class Spider():
    def __init__(self, pos):
        self.body_radius = 60
        self.pos = pos
        self.vel = pygame.Vector2((0.5,0))
        self.color = (150,150,150)

        self.leg1_pos = (self.pos[0]-30, self.pos[1]+30)
        self.leg1 = IKLeg(2, 70, self.leg1_pos)
        self.leg1_target = (self.pos[0]+30, self.pos[1]+130)

        self.target = (self.pos[0]+30, self.pos[1]+130)

    def update_leg_pos(self):
        self.leg1_pos = (self.pos[0]-30, self.pos[1]+30)
        self.leg1.root.start_pos = self.leg1_pos
        
        self.target = (self.pos[0]+50, self.pos[1]+130)

    def move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

    def update(self):
        self.move()
        self.update_leg_pos()
        pygame.draw.circle(screen, self.color, self.pos, self.body_radius)

        color = (255, 255, 100)
        if self.leg1.touching_target:
            color = (100,100,100)

        pygame.draw.circle(screen, color, self.leg1_pos, 10)
        pygame.draw.circle(screen, (255, 0, 0), self.target, 10)

        if not self.leg1.touching_target:
            self.leg1_target = self.target
        self.leg1.update(self.leg1_target)

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

def bound(value, target, bound):
    right_bound = target+bound
    left_bound = target-bound
    if value > right_bound or value < left_bound:
        return False
    return True

spider = Spider([100,250])

while True:
    screen.fill((0,0,0))
    pygame.draw.rect(screen, (100, 255, 150), (0, HEIGHT-50, WIDTH, 50))
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pos = pygame.mouse.get_pos()
    spider.update()

    pygame.display.update()