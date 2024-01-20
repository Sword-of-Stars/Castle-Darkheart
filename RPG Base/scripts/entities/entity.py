import pygame

from scripts.utils.core_functions import collision_list


class Entity(pygame.sprite.Sprite):
    def __init__(self, speed, layer=0):
        pygame.sprite.Sprite.__init__(self)

        self.vel = pygame.Vector2(0,0)
        self.speed = speed
        self.layer = layer


    def normalize_speed(self):
        if self.vel != [0,0]:
            vx, vy = self.vel.normalize()*self.speed
        else:
            vx, vy = 0,0
        return vx, vy

    def move(self, obstacles):
        # Perhaps stop wall hugging from slowing down player/entities
    
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