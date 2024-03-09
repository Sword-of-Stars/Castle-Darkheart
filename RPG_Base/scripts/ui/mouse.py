import pygame

class Mouse():
    def __init__(self):
        mouse = pygame.image.load("data/mouse3.png")
        self.img = pygame.transform.scale_by(mouse, 4).convert_alpha()
        self.img.set_colorkey((255, 255, 255))
        self.rect = mouse.get_rect()

        self.layer = 12

        pygame.mouse.set_visible(False)

    def draw(self, camera):
        camera.display.blit(self.img, self.rect)

    def update(self, camera):
        self.rect.center = pygame.mouse.get_pos()
        camera.to_render(self)