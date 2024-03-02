import pygame

class Button():
    def __init__(self, img, pos, scale=1, sound=None):
        self.img = pygame.image.load(img)
        self.image = pygame.transform.scale_by(self.image, scale).convert_alpha()
        self.rect = self.img.get_rect(x=pos[0], y=pos[1])
        self.glow = pygame.image.load("data/menu_images/glow.png")

        self.sound = sound
        if self.sound != None:
            self.sound = pygame.mixer.Sound("data/sound_effects/heartbeat_hover.wav")

    def update(self, screen):
        screen.blit(self.img, self.rect)