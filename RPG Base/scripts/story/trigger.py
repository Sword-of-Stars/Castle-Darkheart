import pygame, sys

class Trigger():
    def __init__(self, _id, pos):
        self.id = _id
        self.pos = pos
        self.original_rect = pygame.rect.Rect(*pos, 64, 64) #MAGIC
        self.rect = self.original_rect.copy()

        self.active = False

        self.group = "trigger"

    def update(self, camera):
        self.rect.x = self.original_rect.x - camera.x
        self.rect.y = self.original_rect.y - camera.y

    def pass_event(self):
        pass
