import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.original_rect = pygame.Rect(x, y, 1000, 100)
        self.rect = self.original_rect.copy()
        self.color = (0, 255, 0)

    def update(self, camera):
        self.rect.x = self.original_rect.x - camera.x
        self.rect.y = self.original_rect.y - camera.y

        pygame.draw.rect(camera.display, self.color, self.rect)