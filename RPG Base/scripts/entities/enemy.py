import pygame
import math

from scripts.entities.entity import Entity
from scripts.utils.core_functions import prep_image, angle_to, collision_list

# Enemies need (generic) speed, health, damage
# (specific) animation, special attacks, 

class Enemy(Entity):
    def __init__(self, speed):
        Entity.__init__(self, speed=speed)

        self.health = 100

    def move_to(self, pos):
        angle = math.radians(angle_to(self.pos, pos))
        #print(angle)

        self.vel = pygame.Vector2(math.cos(angle), math.sin(angle))


class Wendigo(Enemy):
    def __init__(self, x, y, config=None):
        Enemy.__init__(self, speed=6)

        self.pos = pygame.Vector2(x,y)

        self.layer = -1

        self.img = prep_image(pygame.image.load("data/wendigo_01.png"), 4)
        self.rect = self.img.get_frect(x=x, y=y)

        self.radius = 45
        #self.hitbox = pygame.geometry.Circle(self.rect.x, self.rect.y, self.radius)

        self.just_hit_by = []

    def move_camera(self, camera, dx, dy):
        # Send out to external function later
        self.rect.x -= int(dx * camera.speed)
        self.rect.y -= int(dy * camera.speed)

    def take_hit(self, projectile):
        if projectile not in self.just_hit_by:
            self.just_hit_by.append(projectile)
            self.health -= projectile.damage 

    def update(self, camera, player, obstacles):
        #self.hitbox = pygame.geometry.Circle(self.rect.x, self.rect.y, self.radius)

        # get rid of projectiles that have already hit the enemy
        for projectile in reversed(self.just_hit_by):
            if not projectile.is_alive:
                self.just_hit_by.remove(projectile)

        self.move_to(player.pos)
        self.move(obstacles)

        self.pos[0] = self.rect.centerx + camera.rect.x
        self.pos[1] = self.rect.centery + camera.rect.y
                
        camera.to_render(self)

    def draw(self, camera):
        camera.display.blit(self.img, self.rect)

        pygame.draw.circle(camera.display, (200,200,200), self.rect.center, self.radius, 2)
        pygame.draw.line(camera.display, (255,0,0), self.rect.center, (self.rect.center[0] + self.vel[0]*50,self.rect.center[1] + self.vel[1]*50), 10)
        #pygame.draw.rect(camera.display, (100,100,100), self.rect)