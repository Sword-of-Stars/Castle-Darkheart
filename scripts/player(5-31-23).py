import pygame

from scripts.entity import Entity
from scripts.core_functions import collision_list


class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self, 6)
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = (255, 0, 0)

        #- Handle key presses and movement -#
        self.pressed = {"right":False, "left":False, "up":False,"down":False}
        self.most_recent_press = {"horizontal":'',"vertical":''}

        self.speed = 6
        self.ACCEL = 3.6
        self.DECEL = 3.5
        self.MAXSPEED = 6

    def handle_key_presses(self):
        if self.pressed["right"] and self.most_recent_press["horizontal"] != "left":
            self.vel[0] += self.ACCEL
        elif self.pressed["left"] and self.most_recent_press["horizontal"] != "right":
            self.vel[0] -= self.ACCEL
        if not self.pressed["right"] or self.pressed["left"]:
            if self.vel[0] > 0:
                self.vel[0] -= self.DECEL
                if self.vel[0] < 0:
                    self.vel[0] = 0

            if self.vel[0] < 0:
                self.vel[0] += self.DECEL
                if self.vel[0] > 0:
                    self.vel[0] = 0

        if self.pressed["up"] and self.most_recent_press["vertical"] != "down":
            self.vel[1] -= self.ACCEL
        elif self.pressed["down"] and self.most_recent_press["vertical"] != "up":
            self.vel[1] += self.ACCEL
        if not self.pressed["up"] or self.pressed["down"]:
            if self.vel[1] > 0:
                self.vel[1] -= self.DECEL
                if self.vel[1] < 0:
                    self.vel[1] = 0

            if self.vel[1] < 0:
                self.vel[1] += self.DECEL
                if self.vel[1] > 0:
                    self.vel[1] = 0

    def normalize_speed(self):
        if self.vel != [0,0] and self.vel.magnitude() > self.MAXSPEED:
            vx, vy = self.vel.normalize()*self.MAXSPEED
        else:
            vx, vy = 0,0
        return vx, vy

    def move(self, obstacles):
        #self.vel = pygame.Vector2(0,0) 
        # Note, I'm resetting the player's speed every time this is called. Not bad for now, but consider this later
        self.handle_key_presses()
        vx, vy = self.normalize_speed()

        self.rect.x += vx
        hit_list = collision_list(self.rect, obstacles)
        for tile in hit_list:
            if vx > 0:
                self.rect.right = tile.rect.left
            elif vx < 0:
                self.rect.left = tile.rect.right

        self.rect.y += vy
        hit_list = collision_list(self.rect, obstacles)
        for tile in hit_list:
            if vy > 0:
                self.rect.bottom = tile.rect.top
            elif vy < 0:
                self.rect.top = tile.rect.bottom
        
    def update(self, obstacles, camera):
        self.move(obstacles)
        pygame.draw.rect(camera.display, self.color, self.rect)
