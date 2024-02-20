import pygame
import math
import random

def explosion(pos, num_particles, particle_manager, colors=[(51, 51, 51),(37,37,37)], size=[5,10], speed=[1,4]):
    for i in range(num_particles):
        particle_manager.add_particle(Particle(list(pos), math.radians(random.randint(0,360)), random.randint(*speed), random.choice(colors), random.randint(*size)))

class ParticleManager():
    def __init__(self, WIDTH, HEIGHT):
        self.particles = []

        self.surf = pygame.surface.Surface((WIDTH, HEIGHT))
        self.surf.set_colorkey((0,0,0))
        self.rect = pygame.Rect(0,0,WIDTH,HEIGHT)

        self.layer = 2.5

    def add_particle(self, particle):
        self.particles.append(particle)

    def draw(self, camera):
        camera.display.blit(self.surf, (0,0))
    
    def update(self, camera, dx, dy, obstacles):
        self.surf.fill((0,0,0))
        
        for particle in reversed(self.particles):
            particle.update(camera, dx, dy) # maybe deltatime?

            for obstacle in obstacles:
                if obstacle.rect.collidepoint(particle.pos):
                    particle.alive = False

            if not particle.alive:
                self.particles.remove(particle)
                del particle

            else:
                particle.draw(self.surf)

        camera.to_render(self)

class Particle():
    def __init__(self, pos, angle, speed, color, size, scale=4, gravity=False, target=None):
        self.size = size
        self.surf = pygame.Surface((self.size*2, self.size*2))
        self.surf.set_colorkey((0,0,0))
        pygame.draw.circle(self.surf, color, (self.size, self.size), self.size)
        self.surf = pygame.transform.scale_by(self.surf, scale)

        self.rect = self.surf.get_rect(x=pos[0]-2*size*scale,y=pos[1]-2*size*scale)
        self.pos = pos
        self.angle = angle

        self.speed = speed
        self.vel = pygame.Vector2(math.cos(angle), math.sin(angle))

        self.color = color
        self.scale = scale
        self.gravity = gravity

        self.alive = True

        self.target = target    
        

    def update_surf(self):
        self.surf = pygame.Surface((int(self.size)*2, int(self.size)*2))
        self.surf.set_colorkey((0,0,0))

        self.rect = self.surf.get_rect(x=self.pos[0]-2*int(self.size)*self.scale,
                                       y=self.pos[1]-2*int(self.size)*self.scale)
        pygame.draw.circle(self.surf, self.color, (self.size, self.size), self.size)

        self.surf = pygame.transform.scale_by(self.surf, self.scale)

    def update(self, camera, dx, dy):
        self.size -= 0.1

        if self.size < 0:
            self.alive = False
        else:
            self.update_surf()

            self.rect.x += self.vel[0] * self.speed
            self.rect.y += self.vel[1] * self.speed

            self.pos[0] += self.vel[0] * self.speed
            self.pos[1] += self.vel[1] * self.speed

            if self.target != None:
                self.rect.x += self.target.vel[0]
                self.rect.y += self.target.vel[1]

                self.pos[0] += self.target.vel[0]
                self.pos[1] += self.target.vel[1]


            if self.gravity:
                self.vel[1] += 0.03



    def draw(self, surf):
        surf.blit(self.surf, self.rect.center)


class Spark():
    def __init__(self, pos, angle, speed, color,scale=3,target=None):
        self.pos = pos
        self.angle = angle
        self.speed = speed
        self.scale = scale
        self.color = color
        self.alive = True


        self.size = 100
        self.rect = pygame.rect.Rect(*pos, self.size,self.size)

        self.target = target

    def point_towards(self, angle, rate):
        rotate_direction = ((angle - self.angle + math.pi * 3) % (math.pi * 2)) - math.pi
        try:
            rotate_sign = abs(rotate_direction) / rotate_direction
        except ZeroDivisionError:
            rotate_sing = 1
        if abs(rotate_direction) < rate:
            self.angle = angle
        else:
            self.angle += rate * rotate_sign

    def calculate_movement(self, dt):
        return [math.cos(self.angle) * self.speed * dt, math.sin(self.angle) * self.speed * dt]


    # gravity and friction
    def velocity_adjust(self, friction, force, terminal_velocity, dt):
        movement = self.calculate_movement(dt)
        movement[1] = min(terminal_velocity, movement[1] + force * dt)
        movement[0] *= friction
        self.angle = math.atan2(movement[1], movement[0])
        # if you want to get more realistic, the speed should be adjusted here

    def update(self, camera, dx, dy):
        movement = self.calculate_movement(1)
        self.pos[0] += movement[0] - int(dx * camera.speed)
        self.pos[1] += movement[1] - int(dy * camera.speed)

        if self.target != None:
            self.pos[0] += self.target.vel[0]
            self.pos[1] += self.target.vel[1]

        self.rect.center = self.pos

        # a bunch of options to mess around with relating to angles...
        #self.point_towards(math.pi / 2, 0.02)
        #self.velocity_adjust(0.975, 0.2, 8, dt)
        #self.angle += 0.05

        self.speed -= 0.1

        if self.speed <= 0:
            self.alive = False

    def draw(self, surf):

        points = [
                [self.pos[0] + math.cos(self.angle) * self.speed * self.scale, self.pos[1] + math.sin(self.angle) * self.speed * self.scale],
                [self.pos[0] + math.cos(self.angle + math.pi / 2) * self.speed * self.scale * 0.3, self.pos[1] + math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
                [self.pos[0] - math.cos(self.angle) * self.speed * self.scale * 3.5, self.pos[1] - math.sin(self.angle) * self.speed * self.scale * 3.5],
                [self.pos[0] + math.cos(self.angle - math.pi / 2) * self.speed * self.scale * 0.3, self.pos[1] - math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
                ]
        pygame.draw.polygon(surf, self.color, points)

part_handler = ParticleManager(1200,800)