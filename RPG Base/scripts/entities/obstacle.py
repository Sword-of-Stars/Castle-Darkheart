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

class ObstacleImage(pygame.sprite.Sprite):
    def __init__(self, x, y, img, layer, width=None, height=None):
        pygame.sprite.Sprite.__init__(self)
        self.original_rect = img.get_frect(x=x, y=y)
        self.rect = self.original_rect.copy()
        self.color = (0, 255, 0)

        self.layer = layer
        self.img = img
    
    def draw(self, camera):
        camera.display.blit(self.img, self.rect)

    def update(self, camera):
        self.rect.x = self.original_rect.x - camera.x
        self.rect.y = self.original_rect.y - camera.y

class Asset(pygame.sprite.Sprite):
    def __init__(self, x, y, img, layer, width=None, height=None):
        pygame.sprite.Sprite.__init__(self)
        self.original_rect = img.get_frect(x=x, y=y)
        self.rect = self.original_rect.copy()
        self.color = (0, 255, 0)

        self.layer = layer
        self.img = img
    
    def draw(self, camera):
        camera.display.blit(self.img, self.rect)

    def update(self, camera):
        self.rect.x = self.original_rect.x - camera.x
        self.rect.y = self.original_rect.y - camera.y
