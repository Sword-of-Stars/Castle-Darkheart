import pygame

# To avoid passing 'camera' and 'screen' to every f*cking function, I'll just pass a single camera
# object instead
# All sprites will be drawn on the camera surface, and the camera display will be scaled up to the 
# screen dimensions

class Camera():
    def __init__(self, x, y, width, height, scale=1.0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scale = scale

        self.speed = 0.05

        self.display = pygame.Surface((width, height))

    def fill(self):
        self.display.fill((0,0,0))

    def move(self, player):
        dx = player.rect.x - self.width/2
        dy = player.rect.y - self.height/2
        # calculate new camera position using smoothing function
        self.x += int(dx * self.speed)
        player.rect.x -= int(dx * self.speed)

        self.y += int(dy * self.speed)
        player.rect.y -= int(dy * self.speed)

    def update(self, screen):
        screen.blit(self.display, (0,0))