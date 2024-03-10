import pygame, math

from scripts.entities.obstacle import ObstacleImage
from scripts.story.text_box import TextBox


class Altar(ObstacleImage):
    def __init__(self, x, y, img, layer, msg="", final=False):
        ObstacleImage.__init__(self, x, y, img, layer)

        self.group = "altar"

        self.over = False
        self.clicked = False
        self.found = False

        mask = pygame.mask.from_surface(self.img)
        self.mask = mask.to_surface()
        self.mask.set_colorkey((0,0,0))

        self.halo = pygame.transform.scale_by(pygame.image.load("data/halo.png"), 4).convert_alpha()
        self.halo_rect = self.halo.get_rect()

        self.txt = TextBox(msg[0], msg[1])

        self.found_sound = pygame.mixer.Sound("data/sound_effects/find_hymn.wav")

        self.final = final
        self.near = False

    def draw(self, camera):
        camera.display.blit(self.halo, (self.rect.x-self.halo_rect.width//4-22, self.rect.y+6))
        if self.over:
            pixel = 4
            camera.display.blit(self.mask, (self.rect.x+pixel, self.rect.y))
            camera.display.blit(self.mask, (self.rect.x-pixel, self.rect.y))
            camera.display.blit(self.mask, (self.rect.x, self.rect.y+pixel))
            camera.display.blit(self.mask, (self.rect.x, self.rect.y-pixel))

        camera.display.blit(self.img, self.rect)

    def is_near(self, player):
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        if math.hypot(dy, dx) < 100:
            self.near = True
        else:
            self.near = False


    def is_over(self, mouse):
        if mouse.rect.colliderect(self.rect):
            self.over = True
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                if not self.final:
                    self.txt.reset()
                    self.clicked = True
                    if not self.found:
                        self.found = True
                        self.found_sound.play()
                else:
                    if self.near:
                        self.txt.reset()
                        self.clicked = True
                        if not self.found:
                            self.found = True
                            pygame.mixer.music.stop()
                            self.found_sound.play()
        else:
            self.over = False