import pygame, math

from scripts.utils.core_functions import prep_image, get_images

class Dancer:
    def __init__(self, center, angle, length, k, type=0):
        self.pos = center
        self.center = center
        self.angle = angle
        self.length = length
        self.k = k

        self.frames = [prep_image(x, 4) for x in get_images("data/spirit_02.png")]

        self.frame = 0
        self.fps = 0.2

        self.rect = self.frames[0].get_rect()

        self.x_flip = False
        self.prev_x = 0
        self.prev_y = 0

        self.dt = 0.003
        self.t = 0

        self.layer = 20

        self.type = type

        self.vel = [0,0]

    def move_camera(self, camera, dx, dy):
        # Send out to external function later
        self.rect.x -= int(dx * camera.speed)
        self.rect.y -= int(dy * camera.speed)

    def update(self, camera):
        self.t += self.dt
        self.angle = (self.angle + self.dt) % (2 * math.pi)

        if self.type == 0:
            x = self.length * math.sin(self.k * self.t) * math.cos(self.angle)
            y = self.length * math.sin(self.k * self.t) * math.sin(self.angle)
        elif self.type == 1:
            x = self.length * math.cos(self.k * self.t)
            y = self.length * math.sin(self.k * self.t)

        self.vel = pygame.math.Vector2((x-self.prev_x, y-self.prev_y))

        self.x_flip = self.prev_x > x
        self.prev_x = x
        self.prev_y = y

        self.pos = [self.center[0] + x - self.rect.width/2, self.center[1] + y - self.rect.height/2]
        self.rect.x = self.pos[0] - camera.x
        self.rect.y = self.pos[1] - camera.y

        camera.to_render(self)

    def draw(self, camera):
        self.frame = (self.frame +self.fps)% len(self.frames)
        img = pygame.transform.flip(self.frames[int(self.frame)], self.x_flip, False)
        camera.display.blit(img, self.rect)


def generate_rose(length, k, center):

    dancers = []
    for i in range(0, k):
        dancer = Dancer(
            center=[center[0] + math.cos(2 * math.pi / k * i) * length, center[1] + math.sin(2 * math.pi / k * i) * length],
            angle=2*math.pi / k * i,
            length=length,
            k=k
        )
        dancers.append(dancer)
    return dancers


